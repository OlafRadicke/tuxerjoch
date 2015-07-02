<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
% include('header.tpl', title='Fehler')
  <body>
% include( 'menu_bar.tpl', authenticated=authenticated )

      <div>{{ flashed_message }}</div>

  </body>
</html>
