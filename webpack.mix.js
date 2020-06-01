const mix    = require('webpack-mix');
const srcDir = 'assets';
const outDir = 'app/static';

mix
  .js(`${ srcDir }/js/app.js`, `${ outDir }/js`)
  .sass(`${ srcDir }/sass/app.scss`, `${ outDir }/css`)
  .version()
  .setPublicPath(outDir)
;