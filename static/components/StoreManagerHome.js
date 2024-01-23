export default {
    template: `<div> Welcome Store Manager <button @click = 'downloadResource'> Download Resource </button>
    <span v-if='isWaiting'>...Waiting...</span></div>`,
    data(){
        return {
            isWaiting:false,
        }
    },
    methods: {
        async downloadResource(){
            this.isWaiting=true
            const res = await fetch('/download-csv')
            const data = await res.json()
            if (res.ok) {
                this.isWaiting=false
                const taskId = data["task-id"]
                const intv = setInterval(async() => {
                    const csv_res = await fetch(`/get-csv/${taskId}`)
                    if (csv_res.ok) {
                        clearInterval(intv)
                        window.location.href = `/get-csv/${taskId}`
                    }
                }, 1000)
            }

        },
    },
}