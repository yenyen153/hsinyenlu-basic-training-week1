async function fetchStatistics(event) { //取特定條件下的文章數量
    event.preventDefault();

    const form = document.getElementById("get-statistics-form");
    const formData = new FormData(form);
    let params = new URLSearchParams();

    for (let [key, value] of formData.entries()) {
        console.log(`讀取 Query 參數: ${key} = ${value}`);
        if (value.trim() !== "") {
            params.append(key, value);
        }
    }

    let url = "http://127.0.0.1:8000/statistics";
    if (params.toString()) {
        url += `?${params.toString()}`;
    }

    console.log(`最終 API 請求: GET ${url}`);

    try {
        let response = await fetch(url, { method: "GET" });
        let data = await response.json();

        if (response.ok) {
            document.getElementById("statistics-result").textContent = `總文章數: ${data.post_total}`;
        } else {
            document.getElementById("statistics-result").textContent = `錯誤: ${data.detail}`;
        }
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("statistics-result").textContent = "請求失敗，請檢查 API 或網路連線！";
    }
}

async function fetchPosts(event) { //取特定條件下的文章
    event.preventDefault();

    const form = document.getElementById("get-posts-form");
    const formData = new FormData(form);
    let params = new URLSearchParams();

    formData.forEach((value, key) => {
        if (value.trim() !== "") {
            params.append(key, value);
            console.log(` 讀取 Query 參數: ${key} = ${value}`);
        }
    });

    let url = "http://127.0.0.1:8000/posts";
    if (params.toString()) {
        url += `?${params.toString()}`;
    }

    console.log(`最終 API 請求: GET ${url}`);

    try {
        let response = await fetch(url, { method: "GET" });
        let data = await response.json();

        if (response.ok) {
            updatePostsTable(data);
        } else {
            document.getElementById("posts-table-body").innerHTML = `<tr><td colspan="5">錯誤: ${data.detail}</td></tr>`;
        }
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("posts-table-body").innerHTML = `<tr><td colspan="5">請求失敗，請檢查 API 或網路連線！</td></tr>`;
    }
}


function updatePostsTable(posts) { //呈上的function 要展示出的樣子
    let tableBody = document.getElementById("posts-table-body");
    tableBody.innerHTML = "";

    if (posts.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="4">沒有符合條件的文章</td></tr>`;
        return;
    }

    posts.forEach(post => {
        let row = `<tr>
            <td>${post.id}</td>
            <td>${post.title}</td>
            <td><a href="${post.link}" target="_blank">${post.link}</a></td>
            <td>${post.date}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}


async function fetchPostById(event) { //用id取單篇文章
    event.preventDefault();
    let postId = document.getElementById("post_id").value.trim();
    if (!postId) {
        alert("請輸入文章 ID！");
        return;
    }

    let url = `http://127.0.0.1:8000/posts/${postId}`;
    console.log(`API 請求: GET ${url}`);

    try {
        let response = await fetch(url, { method: "GET" });
        let data = await response.json();

        let resultContainer = document.getElementById("get-post-result");
        resultContainer.innerHTML = "";

        if (response.ok) {

            resultContainer.innerHTML = `
                <table>
                    <tr><th>ID</th><td>${data.id}</td></tr>
                    <tr><th>標題</th><td>${data.title}</td></tr>
                    <tr><th>版面代碼</th><td>${data.board_id}</td></tr>
                    <tr><th>連結</th><td><a href="${data.link}" target="_blank">${data.link}</a></td></tr>
                    <tr><th>發文日期</th><td>${data.date}</td></tr>
                    <tr><th>內容</th><td>${data.content}</td></tr>
                </table>
            `;
        } else {
            resultContainer.innerHTML = `<p style="color: red;">錯誤: ${data.detail}</p>`;
        }
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("get-post-result").innerHTML = `<p style="color: red;">請求失敗，請檢查 API 或網路連線！</p>`;
    }
}

async function deletePostById(event) {//用id刪除文章
    event.preventDefault();
    let postId = document.getElementById("delete_post_id").value.trim();
    if (!postId) {
        alert("請輸入文章 ID！");
        return;
    }

    let url = `http://127.0.0.1:8000/delete/${postId}`;
    console.log(`API 請求: DELETE ${url}`);

    try {
        let response = await fetch(url, { method: "DELETE" });
        let data = await response.json();

        document.getElementById("delete-post-result").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("delete-post-result").textContent = JSON.stringify(data.detail, null, 2);
    }
}

async function createPost(event) { //新增文章
    event.preventDefault();

    const form = document.getElementById("create-post-form");
    const formData = new FormData(form);

    let url = "http://127.0.0.1:8000/api/posts";
    console.log(`API 請求: POST ${url}`);

    let postData = {};
    formData.forEach((value, key) => {
        postData[key] = value.trim();
    });

    if (postData["date"]) {
        postData["date"] = new Date(postData["date"]).toISOString();
    }

    try {
        let response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(postData),
        });

        let data = await response.json();

        let resultElement = document.getElementById("create-post-result");

        if (response.ok) {
            resultElement.textContent = `貼文新增成功！ID: ${data.id}`;
        } else {
            let errorMessage = `錯誤:\n`;
            if (Array.isArray(data.detail)) {
                data.detail.forEach(err => {
                    errorMessage += `- ${err.msg} (${err.loc.join(" → ")})\n`;
                });
            } else {
                errorMessage += `${data.detail || "未知錯誤"}`;
            }
            resultElement.textContent = errorMessage;
        }
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("create-post-result").textContent = "請求失敗，請檢查 API 或網路連線！";
    }
}


async function updatePost(event) { //更新文徵
    event.preventDefault();

    let postId = document.getElementById("update_post_id").value.trim();
    if (!postId) {
        alert("請輸入文章 ID！");
        return;
    }

    const form = document.getElementById("update-post-form");
    const formData = new FormData(form);

    let url = `http://127.0.0.1:8000/api/posts/${postId}`;
    console.log(`API 請求: PUT ${url}`);

    let postData = {};
    formData.forEach((value, key) => {
        postData[key] = value.trim();
    });

    if (postData["date"]) {
        postData["date"] = new Date(postData["date"]).toISOString();
    }

    try {
        let response = await fetch(url, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(postData),
        });

        let data = await response.json();

        if (response.ok) {
            document.getElementById("update-post-result").textContent = `更新成功！文章 ID: ${data.id}`;
        } else {
            let errorMessage = `錯誤:\n`;
            if (Array.isArray(data.detail)) {
                data.detail.forEach(err => {
                    errorMessage += `- ${err.msg} (${err.loc.join(" → ")})\n`;
                });
            } else {
                errorMessage += `${data.detail}`;
            }
            document.getElementById("update-post-result").textContent = errorMessage;
        }
    } catch (error) {
        console.error("API 請求錯誤:", error);
        document.getElementById("update-post-result").textContent = "更新失敗，請檢查 API 或網路連線！";
    }
}



document.getElementById("update-post-form").addEventListener("submit", updatePost);
document.getElementById("create-post-form").addEventListener("submit", createPost);
document.getElementById("get-posts-form").addEventListener("submit", fetchPosts);
document.getElementById("get-statistics-form").addEventListener("submit", fetchStatistics);
document.getElementById("get-post-form").addEventListener("submit", fetchPostById);
document.getElementById("delete-post-form").addEventListener("submit", deletePostById);
