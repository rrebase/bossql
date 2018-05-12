$(document).ready(function () {
    $("#searchTutorials").keyup(function () {

        var filter = $(this).val();


        $(".links li a").each(function () {

            // If the list item does not contain the text phrase fade it out
            if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });

    });
});