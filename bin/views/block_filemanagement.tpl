
    <h3>Bilderverwaltung</h3>
    <h4>Neues Bild hoch laden</h4>
    <p>

        <form action="" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="file_id">ID/Speichrname:</label>
                <input
                    classe="form-control"
                    id="file_id"
                    type="text"
                    placeholder="wunsch ID/Name"
                    name="file_id" />
            </div>
            <div class="form-group">
                <label for="upload">Dateiauswahl:</label>
                <input
                    classe="form-control btn btn-default btn-file"
                    id="upload"
                    type="file"
                    name="upload" />
            </div>
            <button
                class="btn btn-default"
                type="submit"
                name="save"
                value="true">Hoch laden</button>
        </form>

        <h4>Verfügbare Bilder Bild</h4>
        % for filename  in filenames:
        <ul>
            <li>{{ filename }} <a href="../pics/{{ filename }}">anzeigen</a> <a href="../filedelete/{{ filename }}">löschen</a></li>
        </ul>

    </p>
