setInterval(function() {
          fetch('/data_json')
              .then(response => response.json())
              .then(data => {


                  const element = document.getElementById("timestmp")
                  element.innerHTML = data.query.timestamp

                  return data.data
              })
              .then((rate) => {
                      Object.keys(rate).forEach(key =>
                          updateElement({key, value:rate[key]})
                      );
                  }
              )
            }, 1000
          );

      function updateElement(rate) {
            const element = document.getElementById("exc-"+rate.key);
            element.innerHTML = rate.value;
        }