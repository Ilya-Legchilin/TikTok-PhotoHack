function chagePostStatus(id_post,set_status) {
        $.ajax({
        type: "POST",
        cache: false,
        url: "/chagestatus",
        dataType: 'json',
        data: {id_post:id_post,set_status:set_status},
        success: function(response) {
          var json = response
          console.log(json) //json[0].id
        },
        error: function(jqXHR) {
                  alert("error: " + jqXHR.status);
                  console.log(jqXHR);
        }
      });
      console.log(id_post,set_status)
    }

function givePosts(project,start_post,quantity,status) {
          $.ajax({
          type: "POST",
          cache: false,
          url: "/givePosts",
          dataType: 'json',
          data: {project:project,start_post:start_post,quantity:quantity,status:status},
          success: function(response) {
            var json = response
            console.log(json) //json[0].id
          },
          error: function(jqXHR) {
                    alert("error: " + jqXHR.status);
                    console.log(jqXHR);
          }
        });
        console.log(project,start_post,quantity,status)
      }

function commentPost(id_post) {
    comment = document.getElementById(id_post).value;

      $.ajax({
      type: "POST",
      cache: false,
      url: "/commentPost",
      dataType: 'json',
      data: {id_post:id_post,comment:comment},
      success: function(response) {
        var json = response
        console.log(json) //json[0].id
      },
      error: function(jqXHR) {
                alert("error: " + jqXHR.status);
                console.log(jqXHR);
      }
    });
    console.log(comment)

}

element = document.getElementById(id);
