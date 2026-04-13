import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all
});

export default [
  {
    ignores: ['projects/**/*']
  },
  ...compat.config({
    overrides: [
      {
        files: ['*.ts'],
        parserOptions: {
          project: [path.join(__dirname, 'tsconfig.json')],
          createDefaultProgram: true
        },
        extends: [
          'plugin:@angular-eslint/recommended',
          'plugin:@angular-eslint/template/process-inline-templates',
          'plugin:prettier/recommended'
        ],
        rules: {
          '@angular-eslint/component-class-suffix': ['off'],
          '@angular-eslint/prefer-inject': ['off'],
          '@angular-eslint/prefer-standalone': ['off']
        }
      },
      {
        files: ['*.html'],
        extends: [
          'plugin:@angular-eslint/template/recommended',
          'plugin:prettier/recommended'
        ],
        rules: {
          'prettier/prettier': [
            'error',
            {
              parser: 'angular'
            }
          ]
        }
      }
    ]
  })
];
