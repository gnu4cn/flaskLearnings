##前言

请在开始学习Flask之前阅读此内容。本章回答了Flask项目的初衷，及再什么时候使用Flask框架，什么时候又不宜使用此框架。

##“micro”指的是什么

“Micro”并不是说整个的web应用必须放到一个Python文件（尽管这样做是可以的），也不是说Flask功能缺乏。微架构（microframework）中的“微（micro）”指的是Flask框架在以保持核心简单为目的的同时，具备可扩展能力（extensible）。Flask不会为你做出许多决定，比如要采用何种数据库。该框架确定下来采用何种模版引擎，也是很容易更换的。Flask下的所有东西，都取决于开发者，所以Flask可以是你所需要的所有，没有多余的（Flask can be everything you need and nothing you don‘t）。

默认的Flask是不带有数据库抽象层、表单验证或其它任何已存在的库可以完成的功能的（By default, Flask does not include a database abstract layer, form validation or anything else where different libaries already exist can handle that）。取而代之的是，Flask支持很多将这些功能加入到应用，从而看起来是在Flask中得到部署一样的扩展。正是这些大量的扩展，提供了数据库集成、表单验证、上传处理、多种开放认证技术及其它很多功能。Flask可能是“微型（micro）”的，但其已适用于不同需求下的生成用途。

##配置和约定

Flask有着很多带有敏感默认值的配置量，以及在对其入门时的少量约定（Flask has many configuration values, with sensible defaults, and a few conventions when getting started）。在约定下，要将模版和静态文件保存在应用的Python源码树下的子目录中，分别命名为`templates`及`static`的文件夹下。尽管可以不照约定行事，但通常不要那样做，特别是在刚入门时。

##
