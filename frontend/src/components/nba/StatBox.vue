<template>
    <div class="bg-gray-50 p-4 rounded-lg shadow-sm text-center">
        <p class="text-sm text-gray-500 uppercase">{{ label }}</p>
        <p class="text-2xl font-bold">{{ value }}</p>
        <p v-if="subtext" class="text-xs text-gray-400">{{ subtext }}</p>
    </div>
</template>

<script setup>
defineProps({
    label: String,
    value: [String, Number],
    subtext: String,
});
</script>