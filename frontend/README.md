##### _разработка Sayfullin R.R.

Инструкция актуальна для Linux-систем.
========================================================================================================================

1. Проверьте установку Node.js и npm
    $ node -v
    $ npm -v
2. Downloading and installing Node.js and npm
    # Download and install nvm:
        $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    # in lieu of restarting the shell
        $ \. "$HOME/.nvm/nvm.sh"
    # Download and install Node.js:
        $ nvm install 22
    # Verify the Node.js version:
        $ node -v
        $ nvm current
    # Verify npm version:
        $ npm -v

========================================================================================================================
React-приложение, которое будет запрашивать пароль с вашего FastAPI-сервера и отображать его пользователю.
0. Перейдите в основную директорию с помощью команды: 
    $ cd sayfullin/frontend
1. Создаем React-приложение:
    $ npx create-react-app password-generator-client
    $ cd password-generator-client
2. Редактируем src/App.js:
    