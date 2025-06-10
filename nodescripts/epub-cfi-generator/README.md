# epub-cfi-generator - kohico

This version of epub-cfi-generator has been modified to output some more data, for [kohico](https://github.com/simonpacis/kohico)'s use. It is a requirement for the "readest" annotation type output of [kohico](https://github.com/simonpacis/kohico).

## Installation
Make sure you have installed [node](https://nodejs.org). 
 
Then clone the repository to a location where it will stick around.
```sh
git clone https://github.com/simonpacis/epub-cfi-generator
```
 
Cd to the repository and install its dependencies globally.

```sh
npm install -g
```

Make usage.js executable: 
```sh
chmod +x usage.js
```

Install it so you can use it via the terminal:
```sh
sudo ln -s "$(pwd)/usage.js" /usr/local/bin/epub-cfi-generator
```

And you're all set. You don't need to use it, kohico will automatically employ it.

## License
MIT
