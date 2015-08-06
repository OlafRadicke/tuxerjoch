
    <h1>Artikel bearbeiten</h1>
    <p>
        <form action="../edit_article" method="POST">
            <input
                type="hidden"
                name="created"
                value="{{artikle["created"]}}">
            <input
                type="hidden"
                name="rev_id"
                value="{{artikle["_rev"]}}">
            <div class="form-group">
                <label for="pub_status">Status:</label>
                <select class="form-control" id="pub_status" name="pub_status">
                % if artikle["document_type"] == "blog_article":
                  <option value="blog_article" selected>Veröffentlicht</option>
                  <option value="draft_article">Entwurf</option>
                % end
                % if artikle["document_type"] == "draft_article":
                  <option value="blog_article">Veröffentlicht</option>
                  <option value="draft_article" selected>Entwurf</option>
                % end
                </select>
            </div>
            <div class="form-group">
                <label for="uri_id">URI-ID:</label>
                <input
                    class="form-control"
                    id="uri_id"
                    type="text"
                    name="uri_id"
                    value="{{artikle["uri_id"]}}"
                    readonly>
            </div>
            <div class="form-group">
                <label for="title">Überschrift*:</label>
                <input
                    class="form-control"
                    id="title"
                    name="title"
                    type="text"
                    value="{{artikle["title"]}}" >
            </div>
            <div class="form-group">
                <label for="teaser_text">Anrisstext(html)*:</label>
                <textarea
                    class="form-control"
                    id="teaser_text"
                    name="teaser_text"
                    type="text"
                    required >{{artikle["teaser"]}}</textarea>
            </div>
            <div class="form-group">
                <label for="article_text">Anrisstext(html)*:</label>
                <textarea
                    class="form-control"
                    id="article_text"
                    name="article_text"
                    rows="15"
                    required >{{artikle["article_text"]}}</textarea>
            </div>
            <div class="form-group">
                <label for="tags">Schlagwörter:</label>
                <input
                    class="form-control"
                    id="tags"
                    name="tags"
                    type="text"
                    value="{{" ".join(artikle["tags"])}}"
                    required />
            </div>
            <button
                class="btn btn-default"
                type="submit"
                name="save"
                value="true">Speichern</button>
            <button
                class="btn btn-default"
                type="submit"
                name="delete"
                value="true">Artikel löschen</button>
            <a href="../">Abbrechen</a>
        </form>
    </p>
