<template>
    <div class="border rounded-lg p-4 text-center shadow hover:shadow-lg transition-shadow">
        <h4 class="font-bold truncate">{{ player.firstname }} {{ player.lastname }}</h4>
        <p class="text-gray-500">
            #{{ player.leagues.standard?.jersey || 'N/A' }} | {{ player.leagues.standard?.pos || 'N/A' }}
        </p>
    </div>
</template>

<script setup>
defineProps({
    player: {
        type: Object,
        required: true
    }
});
</script>