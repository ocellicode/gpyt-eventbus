[![Status][status-badge]][status-url]


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# gpyt-eventbus

## About

## Getting started
Clone the repository, run `poetry install` in the repository root directory.

## Prerequisites
Python 3.11, pip, poetry.

## Installation
Installation of gpyt-eventbus is handled by poetry during development.

## Usage

Serve the application with `waitress-serve gpyt_eventbus.injection.injector:app`.

### Environment variables
| Variable      | Description          | Default                        |
|---------------|----------------------|--------------------------------|
| `GPYT_DB_DSN` | DSN for the database | `sqlite:///gpyt_eventbus.db` |
| `MIGRATE`     | Run migrations       | `0`                            |
| `LOG_LEVEL`   | Log level            | `INFO`                         |

[contributors-shield]: https://img.shields.io/github/contributors/ocellicode/gpyt-eventbus.svg?style=for-the-badge
[contributors-url]: https://github.com/ocellicode/gpyt-eventbus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ocellicode/gpyt-eventbus.svg?style=for-the-badge
[forks-url]: https://github.com/ocellicode/gpyt-eventbus/network/members
[stars-shield]: https://img.shields.io/github/stars/ocellicode/gpyt-eventbus.svg?style=for-the-badge
[stars-url]: https://github.com/ocellicode/gpyt-eventbus/stargazers
[issues-shield]: https://img.shields.io/github/issues/ocellicode/gpyt-eventbus.svg?style=for-the-badge
[issues-url]: https://github.com/ocellicode/gpyt-eventbus/issues
[license-shield]: https://img.shields.io/github/license/ocellicode/gpyt-eventbus.svg?style=for-the-badge
[license-url]: https://github.com/ocellicode/gpyt-eventbus/blob/master/LICENSE
[status-badge]: https://github.com/ocellicode/gpyt-eventbus/actions/workflows/main.yml/badge.svg
[status-url]: https://github.com/ocellicode/gpyt-eventbus/actions/workflows/main.yml
