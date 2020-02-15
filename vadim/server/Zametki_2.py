{% with messages = get_flashed_messages() %}
    {% if messages %}
        <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endwith %}




<br>{% for post in posts %}
      {% include '_post.html' %}
{% endfor %}
posts = [
    {'author': user, 'body': 'Ты чувствуешь улучшение жизни? Нет? И я нет! А оно есть!'},
    {'author': user, 'body': 'Если вы пару раз дадите человеку взаймы, то он уже постоянно будет учитывать вас при планировании своих доходов.'}
]
https://medium.com/@yameday/python-flask-ajax-simple-example-2302424401de

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!    var json = jQuery.parseJSON(response) !!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
