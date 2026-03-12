<script>
    export default {
        data(){
            return {
                formData: {
                    username: ''
                }
            }
        },
        methods: {
            async loginUser(event){
                event.preventDefault();
                const response = await fetch("http://127.0.0.1:5000/api/login", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        
                        body: JSON.stringify(this.formData)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    console.log("Success:", data);
            }
        }
    }
</script>
<template>
    <div id="form-body">
        <h2>Login Form</h2>
        <form @submit="loginUser">
            <div class="mb-3"> 
                <label for="user-name">User Name: </label>
                <input type="text" v-model="formData.username" name="user-name" class="form-control" id="user-name">
                <br>
                <button class="btn btn-primary">Login</button>
            </div>
        </form>
    </div>
</template>
<style></style>