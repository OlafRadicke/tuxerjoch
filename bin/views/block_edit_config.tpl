
    <h4>Einstellungen</h4>
    <p>
        <form action="" method="POST">
            <input
                type="hidden"
                name="rev_id"
                value="{{global_config["_rev"]}}">

            <div class="form-group">
                <label for="cookie_live_time">Session timeout (sekunden):</label>
                <input
                    class="form-control"
                    id="cookie_live_time"
                    type="number"
                    name="cookie_live_time"
                    value="{{global_config["cookie_live_time"]}}">
            </div>
            <div class="form-group">
                <label for="result_limit">Maximale anzeige Artikel auf der Startseite:</label>
                <input
                    class="form-control"
                    id="result_limit"
                    type="number"
                    name="result_limit"
                    value="{{global_config["result_limit"]}}">
            </div>
            <div class="form-group">
                <label for="new_password">Neues Passwort setzen:</label>
                <input
                    class="form-control"
                    id="new_password"
                    type="password"
                    name="new_password"
                    placeholder="Neues Passwort">
                <br>
                <input
                    class="form-control"
                    id="new_password_verify"
                    type="password"
                    name="new_password_verify"
                    placeholder="Neues Passwort wiederholen">
            </div>
            <button
                class="btn btn-default"
                type="submit"
                name="save"
                value="true">Speichern</button>

            <a href="../">Abbrechen</a>
        </form>
    </p>
