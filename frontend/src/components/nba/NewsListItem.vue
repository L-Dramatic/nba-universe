<template>
    <li class="py-3 border-b last:border-b-0">
        <a :href="article.url" target="_blank" rel="noopener noreferrer"
            class="text-blue-600 hover:underline font-semibold">
            {{ article.title }}
        </a>
        <p class="text-sm text-gray-500 mt-1">Source: {{ article.source.name }}</p>
    </li>
</template>

<script setup>
defineProps({
    article: {
        type: Object,
        required: true
    }
});
</script>