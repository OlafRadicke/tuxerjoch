

    <h4>Bild/Dokument wirklich löschen?</h4>
    <p>

        <form action="" method="post" enctype="multipart/form-data">
            <input
                type="hidden"
                name="filename"
                value="{{filename}}">
            % if filename.split(".")[1] in ["jpg","jpeg","gif","png"]  :
            <img src="../pics/{{ filename }}" class="img-thumbnail">
            % else:
            <a href="../pics/{{ filename }}">{{ filename }}</a>
            <br>
            % end
            <button
                class="btn btn-default"
                type="submit"
                name="save"
                value="true">Löschen</button>
            <a href="../filemanagement">Abbrechen</a>
        </form>



    </p>
