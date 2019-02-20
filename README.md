# 44CON-CFP

[![Requirements Status](https://requires.io/github/rawhex/44CON-CFP/requirements.svg?branch=master)](https://requires.io/github/rawhex/44CON-CFP/requirements/?branch=master) [![Coverage Status](https://coveralls.io/repos/github/rawhex/44CON-CFP/badge.svg?branch=master)](https://coveralls.io/github/rawhex/44CON-CFP?branch=master) [![Build Status](https://travis-ci.org/rawhex/44CON-CFP.svg?branch=master)](https://travis-ci.org/rawhex/44CON-CFP) [![Application Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/rawhex/44CON-CFP) ![Supported versions of Python](https://img.shields.io/badge/Python-3.6-blue.svg) ![Supported versions of Django](https://img.shields.io/badge/Django-2.0-green.svg) [![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)](https://github.com/nimxj/44CON-CFP/blob/master/LICENSE)

## Hey, read this...
This application was designed to replace the CFP system we used for 44CON 2016 and 2017. We wanted something that fit our needs and didn't come with a lot of unnecessary cruft. As it stands, this project is very, *very* early in the development lifecycle and will undoubtedly present a number of bugs and issues if run in a production environment. If you intend to reuse this project for your own conference, I would advise going through the entire codebase manually and evaluating whether it's sufficiently mature for your purposes (there's ~4000 lines of code (as of 2018-02-05) so it's not too significant a task).

## Setup
These are extremely rudimentary instructions to build the development environment - some of which will be relevant for preparing a production environment. Previous experience with a Django project is probably necessary to troubleshoot through setup.

1. Get dependencies for Django: `pip install -r requirements.txt`
1. Copy `.env-sample` to `.env` and update it.
1. Build: `sh build.sh`

## Usage
Some database objects are currently critical for certain pages due to bad coding decisions. This will be rectified in future releases but for now, the singular FrontPage and SubmissionDeadline objects should be generated using the admin interface after creating a superuser account. When created, the admin UI will restrict from creating more objects under these models. Again, this is poor design choice and will be corrected in the future but, for the time being, avoid trying to create more of these objects. The logic of the application shouldn't really be affected if you do but shit happens and it likely will.

## Contribute
Yes, absolutely. Contributions to the project are very welcome. This project is entirely open source and hopefully will eventually become a stable option for conferences looking for a modular, modifiable, and simple CFP. For more information on contributing, please read our [Contribution](https://github.com/nimxj/44CON-CFP/blob/master/LICENSE) doc.

## License
[GPLv3](https://github.com/nimxj/44CON-CFP/blob/master/LICENSE) (c) 2017-2018 Sense/Net Ltd.
