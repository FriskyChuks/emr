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


{% extends 'base.html' %}
{% block content %}


 <!-- <script type="text/javascript">
$(function(){
  $("#myVar").change(function(){
  $("#txtDisplay").val($(this).val());
  });
})
</script> -->

<div class="container">
    <form method="POST" action="">{% csrf_token %}
       {% for request in lab_request %}
        {% if request.test.compound_test.id == 1  %}
            <h1>FBC</h1>
        {% endif %}
        {% if request.test.id == 10  %}
            {{ request.test }}: 
              <select class="form-select" aria-label="Default select example" id="myVar" name="variable">
                <option selected>Select an option</option>
                <option value="Negative">Negative</option>
                <option value="Positive">Positive</option>
              </select>
        {% elif request.test.id == 15 %}
            {{ request.test }}:
            <div class="mb-3">
                <textarea class="form-control" rows="3" id="myVar" name="variable"></textarea>
            </div>
        {% else %}
            {{ request.test }}: 
              <div class="mb-3">
                <input class="form-control" id="myVar" name="variable">
              </div>
        {% endif %}
       {% endfor %} 
       <!-- <input type="text" id="txtDisplay" name="test_id">  -->
    <br><br>
    <input type="submit" id="btnRequest" class="btn btn-success" value="Send Results">
    </form>
</div>

{% endblock %}