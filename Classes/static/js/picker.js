$(function() {
    var start_time = 0;
    var end_time = 0;
    var select_week = 0;

    var office_name = $('div#div_select_office').attr('class').trim();

    selectWeek();
    $('div.weak-container').children().first().addClass('weak-select');

    $('button.timepicker').click(function () {
        var input = parseInt($(this).attr('id'), 10);

        if (start_time == 0) {
            start_time = input;
            $(this).addClass('selected');
        } else if (end_time == 0) {

            if (start_time > input) {
                end_time = start_time;
                start_time = input;
                var btn_id = 'button#' + start_time.toString();
            } else {
                end_time = input;
                var btn_id = 'button#' + end_time.toString();
            }

            $.get($SCRIPT_ROOT + '/canSelect/', {
                  start: start_time,
                  end: end_time,
                  week: select_week,
                  office: office_name,
                  }, function (data, status) {
                    if (data == 'false') {
                        Toast('选中区间有不可用，请重试', '2000');
                    } else {
                        $(btn_id).addClass('selected');
                        if (start_time == end_time) { return; }
                        for (var i = (start_time + 1); i < end_time; i++) {
                            var a = 'button#' + i.toString();
                            $(a).addClass('include');
                        }
                    }
                }
            );
        } else {
            start_time = parseInt($(this).attr('id'), 10);
            end_time = 0;
            $('button.timepicker').removeClass('selected');
            $('button.timepicker').removeClass('include');
            $(this).addClass('selected');
        }
    });


    $('button.office-list').click(function () {
        office_name = $(this).text();
        $('a.dropdown-toggle').text(office_name);
        $('a.dropdown-toggle').append(' <span class="caret"></span>');
        selectWeek();
    });

    $('button.search_btn').click(function () {
      var search = $('input').val();
      if (search) {
          $(location).attr('href', $SCRIPT_ROOT + '/search?query=' + search);
      }
  });

    $('button.week-picker').click(function () {
        select_week = parseInt($(this).attr('offset'), 10);
        $('button.week-picker').removeClass('weak-select');
        $(this).addClass('weak-select');

        start_time = 0;
        end_time = 0;
        $('button.timepicker').removeClass('selected');
        $('button.timepicker').removeClass('include');

        selectWeek();
    });

    $('button.submit').click(function () {
        user_name = $('.user_name').val();
        if (!user_name) {
            Toast('请先输入姓名');
            return
        }

        reason = $('.order_reason').val();
        if (!reason) {
            Toast('请先输入预订用途');
            return
        }

        user_depart = $('.user_deaprt').val();

        if (start_time == 0) {
            Toast('请选择起始时间');
            return
        }

        if (end_time == 0) {
            end_time = start_time;
        }

        $.post($SCRIPT_ROOT + '/submit/', {
            user_name: user_name,
            user_depart: user_depart,
            reason: reason,
            start_hour: start_time,
            end_hour: end_time,
            select_week: select_week,
            office: office_name,
              }, function (data, status) {
                if (data != '') {
                    Toast('预约出错：' + data, '2000');
                } else {
                    Toast('预约成功');
                    setTimeout(function () {
                        $(location).attr('href', $SCRIPT_ROOT + '/');
                    }, 2000);
                }
            }
        );
    });

    $('button.show-list').click(function () {
        $(location).attr('href', $SCRIPT_ROOT + '/orderlist/');
    });

    function selectWeek() {
        $.get($SCRIPT_ROOT + '/getOrdered/', {
            office: office_name,
            week: select_week,
            }, function (data, status) {
                $('button.timepicker').removeAttr('disabled');
                var ordered = data['data'];
                for (let i = 0; i < ordered.length; i++) {
                    let from = ordered[i]['order_from'];
                    let to = ordered[i]['order_to'];
                    for (let i = from; i <= to; i++) {
                        var btn_id = 'button#' + i.toString();
                         $(btn_id).attr('disabled','true');

                    }
                }
            }
        );
    }


    function Toast(msg, duration){
        duration=isNaN(duration)?2000:duration;
        var m = document.createElement('div');
        m.innerHTML = msg;
        m.style.cssText="margin:auto;min-width: 180px;opacity: 0.7;height: 30px;color: rgb(255, 255, 255);line-height: 30px;text-align: center;border-radius: 5px;position: fixed;top: 40%;left: 45%;z-index: 999999;background: rgb(0, 0, 0);font-size: 12px;";
        document.body.appendChild(m);
        setTimeout(function() {
            var d = 0.5;
            m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
            m.style.opacity = '0';
            setTimeout(function() { document.body.removeChild(m) }, d * 1000);
        }, duration);
    }
})