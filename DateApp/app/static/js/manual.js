function hide_alert() {
    $("#alert_syn").hide()
}

function query_periodo(modal) {

    //queries periodo dataset
    periodo_id = $("#periodo_input").val()
    if (periodo_id == null || periodo_id == "") {
        return;
    }

    var url = `${window.location}`;
    if (modal) {
        url = url.replace("/review", "");
        url = url + "/manual/"
    }
    var query = {periodo_id: periodo_id};
    url = url.substring(0, url.lastIndexOf('/')) + "/query_periodo/";

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(query),
        contentType: "application/json;charset=UTF-8",
        success: function(data) {
            fill_with_periodo_data(data["periodo_entry"][0])
        }
    });
}

function fill_with_periodo_data(manual_date) {
    $("#date_start").val(manual_date["date_start"])
    $("#date_end").val(manual_date["date_end"])
    $("#comments").val(manual_date["comments"])
}

function get_values() {
    var country_codes = null;
    var comments = null;
    country_codes = get_selected_countries();

    var manual_date = {
        input_string: $("#input_string").val(),
        notes: $("#notes").val(),
        date_start: $("#date_start").val(),
        date_end: $("#date_end").val(),
        comments: $("#comments").val(),
        countries: country_codes,
        is_date_original: $('#date_original_mm').is(":checked"),
        periodo_id: $('#periodo_input').val()
    };
    // return dictionary with values
    return manual_date;
}

function print_check() {
    var periodo_input = $("#periodo_input").val();
    var input_string = document.getElementById("input_string");
    var manual_date = get_values();
    fill_modal_manual(manual_date);
};

function fill_modal_manual(manual_date) {
    document.getElementById("check_input_string").innerHTML = "Input string: " + manual_date["input_string"];
    document.getElementById("check_notes").innerHTML = "Source: " + manual_date["notes"];
    document.getElementById("check_date_start").innerHTML = "Date start: " + manual_date["date_start"];
    document.getElementById("check_date_end").innerHTML = "Date end: " + manual_date["date_end"];
    document.getElementById("check_countries").innerHTML = "Countries: " + get_selected_countries();
    document.getElementById("check_comments").innerHTML = "Comments: " + manual_date["comments"];
}


function submit_syn(modal) {
    var synonym = {
        original_string: $("#input_syn_original").val(),
        synonym: $("#input_syn_mapped").val(),
        comment: $("#comments_syn").val(),
        is_date_original: $('#date_original_syn').is(":checked")
    };
    console.log(`${window.location}manual_date/`);

    var url = `${window.location}`;
    if (modal) {
        url = url.replace("/review", "");
        url = url + "/manual/"
    }

    $.ajax({
        type: "POST",
        url: url + "submit_synonym/",
        data: JSON.stringify(synonym),
        contentType: "application/json;charset=UTF-8",
    });
    $("#input_syn_original").val("");
    $("#input_syn_mapped").val("");
    $("#comments_syn").val("");
    $('#date_original_syn').prop("checked", false);
    $("#alert_syn").show();
};

function manual_date_valid(manual_date) {
    if (manual_date["input_string"] == "" ||
        manual_date["date_start"] == "" || manual_date["date_end"] == "") {
        return false;
    } else {
        return true;
    }
}

function manual_date(modal) {
    manual_info = get_values();
    var valid = manual_date_valid(manual_info);
    if (!valid && modal) {
        $("#error_manual").show();
        return null;
    }

    console.log(`${window.location}manual_date/`);
    var url = `${window.location}`;
    if (modal) {
        url = url.replace("/review", "");
        url = url + "/manual/"
    }

    $.ajax({
        type: "POST",
        url: url + "manual_date/",
        data: JSON.stringify(manual_info),
        contentType: "application/json;charset=UTF-8",
    });

    if (modal) {
        $("#alert_manual").show();
        $("#error_manual").hide();
    }
};

n_lists = 1

function get_selected_countries() {
string_list = ""
    for (i=1; i <= n_lists; i++) {
        id_input = "#countries_input_" + i;
        country = $(id_input).val();
        code = $(id_input).val().substring(country.length, country.length-2);
        if (country) {
            string_list = string_list + code + ",";
        }
    }
    return string_list.substring(0, string_list.length-1);
}

function remove_country_list() {
    $("#div_list_" + n_lists).remove();
    n_lists = n_lists - 1;
    if (n_lists == 1) {
        $("#div_remove_button").html("")
    }
}

