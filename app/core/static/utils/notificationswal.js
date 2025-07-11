const notificationSwal=(titleText,text,icon,confirmButtonText)=>{
    Swal.fire({
        title: titleText,
        text: text,
        icon: icon,
        confirmButtonText: confirmButtonText
      })
}