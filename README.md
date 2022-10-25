<h1 align="center">Seidr</h1><br>  
<p align="center">A set of extensions for <a href="https://github.com/dpgaspar/Flask-AppBuilder">FlaskAppbuilder</a></p>

## Usage

Using the `SeidrApi` and `Security Apis` provided by **Seidr**, you can leverage the full feature set of
FlaskAppbuilder
decoupled from its Server Side Rendering (ModelView) features. :sparkles:

Comming soon: **Seidr** will allow you to create APIs with [OpenAPI 3.0](https://swagger.io/specification/) based
configuration files.

### Prerequisites

All you need is to install **Seidr**, really...

- Create a virtual environment: `python -m venv venv` (or with your IDE)
- Activate virtual environment: `source venv/bin/activate`
- Install requirements
    - Either `pip install git+https://github.com/dttctcs/seidr.git`
    - Or add `git+https://github.com/dttctcs/seidr.git` to your `requirements.txt` and
      do `pip install -r requirements.txt`

### Get Started

To jump start your application **Seidr** provides a skeleton which you can install with **Seidr's** CLI tool

- Install Skeleton app: `seidr create-app`

You will have the option to install **Seidr Studio**. Besides installing **Seidr Studio** this will add `SeidrIndexView`
to your application.

## Configuration

#### SeidrApi

- This interface is currently the heart of **Seidr**. It basically is an extension
  of [Flask Appbuilder's](https://github.com/dpgaspar/Flask-AppBuilder) `ModelRestApi` which again is an implementation

#### flask_cors

- It can make sense to setup `flask_cors` if you want to access your application from different origins it might make
  sense to setup flask_cors
- For development we recommend to use a proxy.
  [CRA](https://create-react-app.dev/docs/proxying-api-requests-in-development/) provides a configuration
  option for such a case.

#### flask_migrate

WIP

#### Options

Application wide configuration can be leverage through a configuration file.
Options available are [Flask Appbuilder options](https://flask-appbuilder.readthedocs.io/en/latest/config.html) and **
Seidr** specfic options:

| option        | value                                                             | description                                            |
|---------------| ----------------------------------------------------------------- | ------------------------------------------------------ |
| setting_one   | What type is it? String, Integer or a Boolean? Is it constrained? | Add a description and possible caveats for the setting |

> Actually, there are no **Seidr** specific options yet... of:exclamation:

##### Options Example

WIP

---

## Concepts

The main purpose of **Seidr** is to bootstrap a webAPI with the capabilites
of [Flask Appbuilder](https://github.com/dpgaspar/Flask-AppBuilder) detached from its server side renddering
functionalities. Even though one loses the inbuilt UI features of **Flask Appbuilder** we
provide [SeidrUI](https://github.com/dttctcs/seidrui) a React component
library to easily leverage the same functionalities for a React based SPA. We don't provide convenience libraries for
any other JS Framework at the time being. Since **Seidr** is in active development and implemented features are also
subject to change, components and hooks for **SeidrUI** are in constant development as well. Keep in mind that these
features diverge from the UI capabilities of **Flask Appbuilder**  :bulb:


