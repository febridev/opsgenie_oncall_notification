# Opsgenie Oncall Rotation Notification

Send notification to specific google chat space for specific team.

## Tech Stack

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3.12-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![PDM](https://img.shields.io/badge/PDM-%233B82F6.svg?style=for-the-badge&logo=pdm&logoColor=0B3D8D&color=AC75D7)
![.ENV](https://img.shields.io/badge/env-%233B82F6.svg?style=for-the-badge&logo=.env&logoColor=0B3D8D&color=ECD53F)

## Installation

### Clone Repository

```bash
git clone https://github.com/febridev/opsgenie_oncall_notification.git
```

### Set Environment Value For Token Opsgenie

copy file `env.example` to `.env`

```bash
cp env.example .env
```

Edit file `.env` add replace `<your_token>` with your token

```bash
vi .env
```

Add your team and space url if needed
[Setup Google Chat Webhooks](https://developers.google.com/workspace/chat/quickstart/webhooks)

```bash
vi src/opsgenie_oncall_notification/gchat_space.json
```

Add your userid from google chat and your email if needed

[Get Google Chat UserId](https://developers.google.com/workspace/chat/api/reference/rest)

```bash
vi src/opsgenie_oncall_notification/gchat_userid.json
```

### Build Image On Docker

```bash
cd opsgenie_oncall_notification
docker image build --no-cache -t opsgenie_oncall_notification:1.0 .
```

### Create container and start the application

```bash
cd opsgenie_oncall_notification
docker compose up -d
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT
