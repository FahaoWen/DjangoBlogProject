window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',

    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })


    $("#submit-btn").click(function (event) {
        // prevent the default of the button so it will not use the form function

        event.preventDefault();

        let title = $("input[name ='title']").val();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('/blog/pub',{
            method: 'POST',
            data: {title, category, content, csrfmiddlewaretoken},
            success: function (result) {
               if (result.code===200){
                   let blog_id = result['data']['blog_id']
                   window.location = '/blog/detail/'+blog_id;
               }else{
                   alert(result['message']);
               }
            }
        })
    });


}