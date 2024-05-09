$(document).ready(function() {
    // 当文档加载完成后执行的函数
    $('#airport-form').on('submit', function(event) {
        // 阻止表单提交的默认行为
        event.preventDefault();

        var form = $(this);
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            dataType: 'json',
            success: function(response)
            {
                if (response.redirect) {
                    // 服务器返回了一个重定向URL，执行重定向
                    window.location.href = response.redirect;
                } else {
                    // 处理其他成功情况
                    $('#loading-status').text('加载成功');
                }
            },
            error: function()
            {
                $('#loading-status').text('加载失败');
            },
            beforeSend: function()
            {
                $('#loading-status').text('加载中...');
            }
        });
    });
});

//用于获取excel的js
// $(document).ready(function() {
//     // 当文档加载完成后执行的函数
//     $('#airport-form').on('submit', function(event) {
//         // 阻止表单提交的默认行为
//         event.preventDefault();

//         var form = $(this);
//         var url = form.attr('action');

//         $.ajax({
//             type: "POST",
//             url: url,
//             data: form.serialize(),
//             dataType: 'binary',
//             xhrFields: {
//                 'responseType': 'blob'
//             },
//             success: function(blob, status, xhr)
//             {
//                 // 获取响应头中的Content-Disposition字段
//                 var contentDisposition = xhr.getResponseHeader('Content-Disposition');
//                 var filename = "";
//                 if (contentDisposition) {
//                     // 从Content-Disposition中提取文件名
//                     var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
//                     var matches = filenameRegex.exec(contentDisposition);
//                     if (matches != null && matches[1]) { 
//                         filename = matches[1].replace(/['"]/g, '');
//                     }
//                 }

//                 // 创建一个链接元素并设置下载属性
//                 var link = document.createElement('a');
//                 link.href = window.URL.createObjectURL(blob);
//                 link.download = filename;
//                 link.click();
//                 $('#loading-status').text('加载成功');
//             },
//             error: function()
//             {
//                 $('#loading-status').text('加载失败');
//             },
//             beforeSend: function()
//             {
//                 $('#loading-status').text('加载中...');
//             }
//         });
//     });
// });