
    <h1>Neuer Artikel</h1>
    <p>
        <form action="" method="POST">
            <div class="form-group">
                <label for="pub_status">Status:</label>
                <select class="form-control" id="pub_status" name="pub_status">
                  <option value="blog_article">Veröffentlicht</option>
                  <option value="draft_article" selected>Entwurf</option>
                </select>
            </div>
            <div class="form-group">
                <label for="uri_id">URI-ID:</label>
                <input
                    class="form-control"
                    id="uri_id"
                    type="text"
                    name="uri_id"
                    placeholder="wunsch uri" >
            </div>
            <div class="form-group">
                <label for="title">Überschrift*:</label>
                <input
                    class="form-control"
                    id="title"
                    name="title"
                    type="text"
                    placeholder="Überschrift" >
            </div>
            <div class="form-group">
                <label for="teaser_text">Anrisstext(html)*:</label>
                <textarea
                    class="form-control"
                    id="teaser_text"
                    name="teaser_text"
                    type="text"
                    placeholder="Anrisstext"
                    required ></textarea>
            </div>
            <div class="form-group">
                <label for="article_text">Anrisstext(html)*:</label>
                <textarea
                    class="form-control"
                    id="article_text"
                    name="article_text"
                    rows="15"
                    placeholder="Artikeltext"
                    required ></textarea>
            </div>
            <div class="form-group">
                <label for="tags">Schlagwörter:</label>
                <input
                    class="form-control"
                    id="tags"
                    name="tags"
                    type="text"
                    placeholder="Schlagwörter"
                    required />
            </div>
            <button class="btn btn-default" type="submit">Speichern</button>
        </form>
    </p>
