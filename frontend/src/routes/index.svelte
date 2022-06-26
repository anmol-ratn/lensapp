<script>
    import { Button, Icon } from "sveltestrap";
    import FormData from "form-data";

    let fileinput;
    let src;
    let text;
    let displayText;

    const onFileSelected = (e) => {
        src = null;
        text = null;
        displayText = true;

        let image = e.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(image);
        reader.onload = (e) => {
            src = e.target.result;
        };
        const dataArray = new FormData();
        dataArray.append("file", image);

        fetch("http://" + location.hostname + ":3001", {
            method: "POST",
            body: dataArray,
        })
            .then((response) => response.json())
            .then(({ data }) => {
                text = data;
                displayText = null;
            })
            .catch((error) => {
                console.log(error);
                console.log("API Call Failed");
            });
    };
</script>

<div id="app">
    <h1 class="text">Label Your Image</h1>
    {#if src}
        <img {src} alt="placeholder" id="image-space" />
    {:else}
        <img src="placeholder.png" alt="placeholder" id="image-space" />
    {/if}
    {#if displayText}<p>Loading...</p>{/if}
    {#if text}
        <ol>
            <li>{text[0]}</li>
            <li>{text[1]}</li>
            <li>{text[2]}</li>
        </ol>
    {/if}
    <Button
        on:click={() => {
            fileinput.click();
        }}>Upload/Capture Image <Icon name="upload" /></Button
    >
    <input
        style="display:none"
        type="file"
        accept="image/*"
        capture
        on:change={(e) => onFileSelected(e)}
        bind:this={fileinput}
    />
</div>

<style>
    #app {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-flow: column;
        margin-top: 3em;
    }

    .text {
        font-family: Arial, Helvetica, sans-serif;
    }

    #image-space {
        margin: 1em;
        height: 224px;
        width: 224px;
        outline: auto;
    }
</style>
