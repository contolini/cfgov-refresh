const assert = require( 'assert' );

describe( 'the cf.gov homepage', () => {
  it( 'should not have changed visually for medium-ish screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 1024, 768 );
    browser.saveFullPageScreen( 'homepage' );
    expect( browser.checkFullPageScreen( 'homepage' ) ).toEqual( 0 );
  } );
  it( 'should not have changed visually for large-ish screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 1280, 1024 );
    browser.saveFullPageScreen( 'homepage' );
    expect( browser.checkFullPageScreen( 'homepage' ) ).toEqual( 0 );
  } );
} );
