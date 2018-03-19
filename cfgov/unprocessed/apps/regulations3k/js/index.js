// This is a placeholder JS file. Its contents will change.

const module1 = require( './module1.js' );
const module2 = require( './module2.js' );

const app = {
  init: () => {
    module1.init();
    module2.init();
  }
};

app.init();
