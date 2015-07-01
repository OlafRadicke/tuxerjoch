<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>Neuer Artikel</title>
  </head>
  <body>
    <p>
 % if flashed_message:
      <div>{{ flashed_message }}</div>
 % end
    </p>
    <h1>Neuer Artikel</h1>
    <p>
        <form action="" method="POST">
        URI-ID:<br>
        <input type="text" name="uri_id" placeholder="wunsch uri" >
        <br>
        Überschrift*:<br>
        <input type="text" name="title" placeholder="Überschrift" required  >
        <br>
        Artikel*:<br>
        <textarea name="article_text" cols="80" rows="5" placeholder="Artikeltext" required ></textarea>
        <br>
        Schlagwörter:<br>
        <input id="firstname"  name="tags" type="text" placeholder="Schlagwörter" required />
        <br>
        <button type="submit">Speichern</button>
        </form>
    </p>
  </body>
</html>
