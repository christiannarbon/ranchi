import pluginVue from 'eslint-plugin-vue'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default [
  ...pluginVue.configs['flat/essential'],
  skipFormatting,
  {
    rules: {
      'vue/multi-word-component-names': 'off'
    }
  }
]
