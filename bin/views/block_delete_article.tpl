    <h1>Artikel Löschen?</h1>
    <p>
        <form action="delete_article" method="POST">
            <input
                type="hidden"
                name="rev_id"
                value="{{artikle["_rev"]}}">
            <input
                type="hidden"
                type="text"
                name="uri_id"
                value="{{artikle["uri_id"]}}">
            <p>
                Den Artikel <i>&quot;{{artikle["title"]}}&quot;</i>  wirklich (unwiederbringlich) löschen?
            </p>
            <p>
                <button
                    class="btn btn-default"
                    type="submit"
                    name="delete"
                    value="true">Artikel löschen</button>
                <a href="../">Abbrechen</a>
            </p>
        </form>
    </p>
