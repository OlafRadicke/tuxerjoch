<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
% include('header.tpl', title='Login')
  <body>
% if flashed_message:
      <div>{{ flashed_message }}</div>
% end
% include( 'menu_bar.tpl', authenticated=authenticated )
    <h1>Login</h1>
    <p>
        <form action="/login" method="post">
            Passwort: <input name="password" type="password" />
            <br>
            <button type="submit">Login</button>
        </form>
    </p>
  </body>
</html>
