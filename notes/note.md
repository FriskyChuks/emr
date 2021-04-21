<!-- Link for Django filter -->
https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-model

{% url 'home' as home_url %}
{% url 'contact' as contact_url %}
{% url 'registration' as registration_url %}
{% url 'auth_login' as login_url %}
{% url 'auth_logout' as logout_url %}
{% url "patient_registration" as patient_registration_url %}
{% url "clinic_view" as clinic_url %}
{% url "ward_view" as ward_url %}


var TableData;
        TableData = storeTblValues()
        TableData = $.toJSON(TableData);

        function storeTblValues()
        {
            var TableData = new Array();

            $('#prescription-table tr').each(function(row, tr){
                TableData[row]={
                    "taskNo" : $(tr).find('td:eq(0)').text()
                    , "item-id" :$(tr).find('td:eq(1)').text()
                    , "title" : $(tr).find('td:eq(2)').text()
                    , "type" : $(tr).find('td:eq(3)').text()
                    , "qty-per-intake" :$(tr).find('td:eq(4)').text()
                    , "times-daily" : $(tr).find('td:eq(5)').text()
                    , "no-of-days" : $(tr).find('td:eq(6)').text()
                }    
            }); 
            console.log(TableData)
            TableData.shift();  // first row will be empty - so remove
            
            return TableData;
        }