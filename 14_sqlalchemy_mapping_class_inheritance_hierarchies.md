#SQLAlchemy的映射类继承层次

##Mapping Class Inheritance Hierarchies

>译者注：此特性为SQLAlchemy的高级特性，可以解决一些复杂关系问题。

SQLAlchemy提供了三种形式的继承：**单一数据表继承，single table inheritance**，这种继承下，多个不同类型的类，都由一个单一数据表来表示；**具体数据表继承，concrete table inheritance**，此种继承中各种类型的类，都由独立数据表来表示；而**连接数据表继承，joined table inheritance**，则其中的类层次在依赖数据表之间是拆分了的，各个类都有代表其本身的数据表，这些数据表又都仅包含属于该类的本地属性值。

继承的最常见形式，就是单一及连接数据表，同时具体继承还有着更多的配置挑战。

当有映射器（mappers）配置在继承关系中时，SQLAlchemy就有着多态性地装入元素的能力，就意味着单一的查询就能返回多种类型的对象（<quote>译者注：实际应用中，很多时候都需要这样的能力</quote>）。

##连接数据表继承，Joined Table Inheritance

在连接数据表继承中，每个缘自某特定类清单父类的类，都由一个唯一数据表表示出来。某个特定实例的全部属性集，是由继承路径上所有数据表属性的结合。下面，我们首先定义了`Employee`类。此数据表将包含一个主键列（或多个列），以及一个由`Employee`所表示的每个属性。本例中就仅是`name`：

```python
class Employee(db.Model):

    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }

```

那些被映射的数据表，同样有着一个名为`type`的列。此列的目的，就是作为**辨别器，discriminator**来发挥作用的，同时其保存了一个行所表示的对象的类型。该列可以是任何的数据类型，不过字符串和整数是最常见的类型。

>注意：

>目前，**仅能设置一个辨别器**，也通常是层次中最为基础的类上设置该辨别器。“级联（Cascading）”的多态列也尚不支持。

而也仅在需要多态性装入（polymorphic loading）时，才需要该辨别器列，不过多态性装入也正是通常需要的功能。并非必须要将辨别器列包含在该基类映射数据表中，且也可以在查询到该类时，将其定义在一个派生的`select`语句上；但这样做就会是另一种更为复杂的配置情形了。

映射经由`__mapper_args__`字典，接收到额外的一些参数。这里的`type`列是作为辨别器列，显式声明出来的，同时这里还给出了`employee`的**多态身份，polymorphic identity**；这就是将要存储在该类的实例中的多态辨别器列（the polymorphic discriminator column）中的值。

后面就定义出`Employee`的子类`Engineer`和`Manager`。其各自包含了一些其所表示的特定子类属性的列。每个表也必须包含一个主键列（或几个主键列），以及在大多数情况下的一个到父数据表的外键引用（a foreign key reference）。

```python
class Engineer(Employee):

    __tablename__ = 'engineer'

    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    engineer_name = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'engineer'
    }

class Manager(Employee):

    __tablename__ = 'manager'

    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    manager_name = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }
```

将同样的列用作主键角色，又同时将其作为到父数据表的外键，还要将该列命名为与父数据表中一样，是标准做法。但这些做法都是可选的。可以使用分开的列，分别作为主键及父关系，同时列也可以命名为与父中的列不同的名字，甚至可以在父及子数据表直接指定不同的连接条件（a custom join condition），而不是使用一个外键。

>关于连接继承的主键问题

>连接数据表继承配置的一个天然影响，就是任何被映射的对象的身份，都完全可以从基类数据表找出。这有着明显的好处，所以SQLAlchemy总是考虑仅将基类数据表的主键作为连接继承类的主键列。换句话说，`engineer`及`manager`数据表的`id`列，并不用于`Engineer`及`Manager`对象的查找--而只会考虑`employee.id`中的值。当然`engineer.id`及`manager.id`对于总体的模式操作，仍然是很重要的，因为它们将在某个语句中的父行确定后，用于查找连接行（locate the joined row）。

在连接继承映射完成后，对`Employee`的查询，就将返回结合了`Employee`、`Engineer`以及`Manager`的对象。而新近保存的`Engineer`、`Manager`及`Employee`对象，就会使用相应的`engineer`、`manager`及`employee`，自动生成`employee.type`列。

###对所查询数据表的基本控制，Basic Control of Which Tables are queried

函数[`orm.with_polymorphic`](http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#sqlalchemy.orm.with_polymorphic)以及[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query)的[`with_polymorphic`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.with_polymorphic)方法，都会对[`Query`]所进行select操作的指定数据表。一般来讲，像下面这样的查询：

```python
session.query(Employee).all()
```

就仅会从`employee`数据表中进行select操作。当刚从数据库装入时（when loading fresh from the database），使用的如下的SQL，这里的连接数据表设置将仅从父数据表进行查询：

```sql
SELECT employee.id AS employee_id,
    employee.name AS employee_name, employee.type AS employee_type
FROM employee
[]
```

因为属性是请求自这些表示在`engineer`或`manager`子数据表中的`Employee`对象，这里的第二次装入，如数据尚未装入，则就是对那个有关的行的那些列进行执行的。因此，就可以看到执行了下面的这些SQL后所返回的对象：

```sql
SELECT manager.id AS manager_id,
    manager.manager_data AS manager_manager_data
FROM manager
WHERE ? = manager.id
[5]
SELECT engineer.id AS engineer_id,
    engineer.engineer_info AS engineer_engineer_info
FROM engineer
WHERE ? = engineer.id
[2]
```

这在执行少量条目查询时，比如使用[`Quey.get()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get)，没有问题，因为并没有将连接的数据表的全部范围都无必要地拉入到SQL语句中。但在查询一个较大范围的、由许多类型构成的多个行时，就会打算积极将一些或是所有的连接数据表连接起来。那么该`with_polymorphic`特性，就提供了此类查询。

可以使用函数`orm.with_polymorphic`, 来建立一个表示结合了到继承的数据表的外部连接基类数据表的select查询的新的别名类（a new aliased class which represents a select of the base table combained with outer joins to each of the inheriting tables）：

```python
from sqlalchemy.orm import with_polymorphic
eng_plus_manager = with_polymorphic(Employee, [Engineer, Manager])
query = db.session.query(eng_plus_manager)
```

这些代码生成一个连接了`employee`数据表到`engineer`及`manager`数据表的查询，作用如下：

```sql
SELECT employee.id AS employee_id,
    engineer.id AS engineer_id,
    manager.id AS manager_id,
    employee.name AS employee_name,
    employee.type AS employee_type,
    engineer.engineer_info AS engineer_engineer_info,
    manager.manager_data AS manager_manager_data
FROM employee
    LEFT OUTER JOIN engineer
    ON employee.id = engineer.id
    LEFT OUTER JOIN manager
    ON employee.id = manager.id
[]
```

`orm.with_polymorphic`所返回的实体，是一个[`AliasedClass`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.util.AliasedClass)对象，其可像其它别名一样，用在某个`Query`，包含了在`Employee`类上的那些命名熟悉。在这个示例中，`eng_plus_manager`成为了用于对上面的三向外部连接的引用实体（the entity that use to refer to the three-way outer join above）。其同时包含了类清单中所命名的各个类的命名空间，因此就可以访问到这些特定子类的属性。下面的例子，演示了对`eng_plus_manager`中`Engineer`以及`Manager`属性的访问：

```python
eng_plus_manager = with_polymorphic(Employee, [Engineer, Manager])
query = db.session.query(eng_plus_manager).filter(
    or_(
        eng_plus_manager.Engineer.engineer_name=='x',
        eng_plus_manager.Manager.manager_name=='y'
)
)
```

>译者注：这里的`or_`是一个函数（方法），使用前需要从`sqlalchemy`导入进来。

`orm.with_polymorphic`方法接受单一类或映射器、类及映射器清单，或者字符串`'*'`以表明所有子类：

```python
# join to the engineer table
entity = with_polymorphic(Employee, Engineer)

# join to the engineer and manager tables
entity = with_polymorphic(Employee, [Engineer, Manager])

# join to all subclass tables
entity = with_polymorphic(Employee, '*')

# use the 'entity' with a Query object
session.query(entity).all()
```

该方法还接受第三个参数`selectable`，该参数取代自动的连接建立并由提供的selectable参数来代替select操作（It also accepts a third argument `selectable` which replaces the automatic join creation and instead selects directly from the selectable given）。该特性通常与稍后要介绍到的‘具体（concrete）’继承一起使用，但可在需要使用多态性装入的特殊SQL使用中，与任何的继承一起应用：

```python
# custom selectable
employee = Employee.__table__
manager = Manager.__table__
engineer = Engineer.__table__
entity = with_polymorphic(
            Employee,
            [Engineer, Manager],
            employee.outerjoin(manager).outerjoin(engineer)
        )

# use the 'entity' with a Query object
session.query(entity).all()
```

请注意如仅需装入单一的子类型（subtype），比如仅是`Engineer`对象，那么就不需要使用`orm.with_polymorphic`, 因为可以直接对`Engineer`类进行查询。

[`Query.with_polymorphic`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.with_polymorphic)有着与`orm.with_polymorphic`同样的目的，除了在其使用模式中没有那么灵活外，因为其仅应用到第一个的完整映射，这就在`Query`中影响到那个类或目标类的所有事件（except is not as flexible in its usage patterns in that it only applies to the first full mapping, which then impacts all occurrences of that class or the subclasses within the Query）。作为简单示例，可以认为其较为简洁：

```python
db.session.query(Employee).with_polymorphic([Engineer, Manager]).\
    filter(or_(Engineer.engineer_name=='w', Manager.manager_name=='q'))
```

>版本0.8中的新特性：`orm.with_polymorphic`，一个`Query.with_polymorphic`方法的改进版本。

映射器也接受`with_polymorphic`作为一个配置性参数，因此连接样式的装入就可自动执行了（the joined-style load will be issued automaticly）。此参数可以是字符串`'*'`、一个类清单，或包含了它们的一个元组，后面跟随一个selectable参数：

```python
class Employee(db.Model, ModelMixin):

    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type,
        'with_polymorphic': '*'
    }

class Engineer(Employee):

    __tablename__ = 'engineer'

    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'engineer'
    }

class Manager(Employee):

    __tablename__ = 'manager'

    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }

```

上面的映射将生成一个类似于对`Employee`对象的每次`with_polymorphic`查询的查询。

而使用`orm.with_polymorphic`或`Query.with_polymorphic`，将覆盖映射器级别的`with_polymorphic`设置（the mapper-level `with_polymorphic` setting）。

>`sqlalchemy.orm.with_polymorphic(base, classes, selectable=False, flat=False, polymorphic_on=None, aliased=False, innerjoin=False, _use_mapper_path=False, _existing_alias=None)`

生成一个指定出所给的基类的后代映射器的指定列的`AliasedClass`结构体（Produce an `AliasedClass` construct which specifies columns for descendant mappers of the given base）。

>版本0.8中的新特性：`orm.with_polymorphic`是对既有的`Query`方法`Query.with_polymorphic`的补充，该方法有着同样目的，但在使用中不那么灵活。

此方法的使用，将确保各个后代映射器的数据表是包括在`FROM`条文（the `FROM` clause）中的，且将允许对这些数据表应用`filter()`规则。而结果实例也已将这些列进行了装入，因此不再需要对这些列的“后取（post fetch）”操作。

请参见[Basic Control of Which Tables are Queried](http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#with-polymorphic)中的例子。

###参数：

- **base** -- 要进行别名操作的基类（Base class to be aliased）。

- **classes** -- 单一的类或映射器，或类/映射器的清单，这些类或映射器都是继承自基类的。此外，该参数也可以是字符串`'*'`，此时所有后代的被映射类都将加入到`FROM`条文（the FROM clause）。

- **aliased** -- 在此参数为`True`时，selectable参数将被封装在一个别名中，也就是`(SELECT * FROM <fromclauses>) AS anon_1`。当在使用`with_polymorphic()`方法创建一个在不支持放入括号中的连接的后端（a backend that does not support parenthesized joins）上，比如SQLite及老版本的MySQl，的`JOIN`目标时，这是重要的。

- **flat** -- 这是一个逻辑值参数，将传递给`FromClause.alia()`调用，由此`Join`对象的别名就不包含一个封闭的`SELECT`了。此参数可在许多情形下带来更高的效率。某个嵌套的`JOIN`上的`JOIN`，将被重写为对某个别名的在后端上的不支持此语法的`SELECT`子查询的`JOIN`（A JOIN against a nested JOIN will be rewritten as a JOIN against an aliased SELECT subquery on backends that do not support this syntax）。

将`flat`设置为`True`就意味着`aliased`参数也是`True`。

>这是版本0.9.0中的新特性。

>参见[`Join.alias()`](http://docs.sqlalchemy.org/en/latest/core/selectable.html#sqlalchemy.sql.expression.Join.alias)

- **selectable**，该参数是将用在生成的`FROM`条文处的一个数据表或`select()`语句。在所需类使用了具体数据表继承（concrete table inheritance），因为当前SQLAlchemy无法在数据表之间自动生成`UNIONs`。如使用了该参数，其就必须表示经由每个映射类所映射的数据表及列的完整集合。否则那些未计入的映射列就将导致其数据表直接追加到`FROM`条文，这就将造成错误的查询结果。

- **polymorphic_on** -- 该参数是一个用作“辨别器（discriminator）”的列，提供给`selectable`。如未提供此参数，当基类有着`polymorphic_on`属性时，就默认使用基类的`polymorphic_on`属性。此参数对于那些默认不具有多态装入行为（do not have polymorphic loading behavior by default）的映射来说，是有用的。

- **innerjoin** -- 在此参数为`True`时，就会使用一个`INNER JOIN`。只会在仅查询某个指定的子类型时，才指定此参数（This should only be specified if querying for one specific subtype only）。

##对所查询数据表的高级控制

`with_polymorphic`函数（`orm.with_polymorphic`及`Query.with_polymorphic`）在简单场景下工作得很好。但在诸如某人想要只输出子类数据表而并非父数据表，这样的数据表输出时，就要使用到直接控制（direct control of table rendering is called for, such as the case when one wants to render to only the subclass table and not the parent table）。

下面的用例同通过直接使用映射的`Table`对象实现。比如，要查询特定条件下`employees`的名字：

```python
engineer = Engineer.__table__
manager = Manager.__table__

db.session.query(Employee.name).\
    outerjoin((engineer, engineer.c.employee_id==Employee.employee_id)).\
    outerjoin((manager, manager.c.employee_id==Employee.employee_id)).\
    filter(or_(Engineer.engineer_info==`w`, Manager.manager_data==`q`))
```


