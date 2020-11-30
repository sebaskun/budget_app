<template>
    <div>
        <transition name="fade" mode="out-in" appear>
            <keep-alive>
                <app-dashboard></app-dashboard>
            </keep-alive>
        </transition>
    </div>
</template>

<script>

import Dashboard from "./components/Dashboard.vue"

export default {
    components: {
      'app-dashboard': Dashboard,
    },
    name: 'app'
}
</script>
