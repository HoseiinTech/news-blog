function like(pk) {
    var element = document.getElementById('like')
    var element2 = document.getElementById('like-out')
    $.get(`/news/like/${pk}/`).then(response => {
        if (response['result'] === 'liked') {
            element.className = "love active"
            element2.className = "ion-android-favorite"
        } else {
            element.className = "love"
            element2.className = "ion-android-favorite-outline"
        }
    })
}