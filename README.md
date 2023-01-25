# Seidr

A set of extensions for [Flask-AppBuilder](https://github.com/dpgaspar/Flask-AppBuilder)

## Concept

The main purpose of **Seidr** is to bootstrap a web API with the capabilities
of [Flask-AppBuilder](https://github.com/dpgaspar/Flask-AppBuilder) detached from its server side rendering
functionalities. Even though one loses the inbuilt UI features of **Flask Appbuilder** we
provide [seidr-react](https://github.com/dttctcs/seidr-react), a React component library to easily leverage the same
functionalities for a React based SPA. We don't provide convenience libraries for any other JS Framework at the time
being. Since **Seidr** is in active development and implemented features are also subject to change, components and
hooks for **SeidrUI** are in constant development as well. Keep in mind that these features diverge from the UI
capabilities of **Flask Appbuilder**.

## Installation

```shell
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/dttctcs/seidr.git
```

## Get Started

To jump start your application, **Seidr** provides a skeleton which you can install with **Seidr's** CLI tool.

Please be aware, that the following command should only be used in a fresh working directory.

```shell
seidr create-app
```

## Configuration

### SeidrApi

This interface is currently the heart of **Seidr**. It basically is an extension
of [Flask-AppBuilder's](https://github.com/dpgaspar/Flask-AppBuilder) `ModelRestApi`.

```python
from flask_appbuilder import Model
from sqlalchemy import Column, Integer
from seidr.interfaces import SeidrApi, SQLAInterface
from app import appbuilder


class ExampleModel(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)


class ExampleApi(SeidrApi):
    resource_name = "test"
    datamodel = SQLAInterface(ExampleModel)


# 
appbuilder.add_api(ExampleApi)
```

#### Quick filters

TODO

#### Related APIs

TODO

### flask_cors

- It can make sense to setup `flask_cors` if you want to access your application from different origins
- For development, we recommend to use a
  proxy. [CRA](https://create-react-app.dev/docs/proxying-api-requests-in-development/)
  provides a configuration option for such a case.