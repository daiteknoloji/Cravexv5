module.exports = {
    sourceMaps: true,
    presets: [
        "@babel/preset-react",
        [
            "@babel/preset-env",
            {
                targets: [
                    "last 2 Chrome versions",
                    "last 2 Firefox versions",
                    "last 2 Safari versions",
                    "last 2 Edge versions",
                ],
                // CRITICAL: Exclude class-properties from preset-env
                // It will be added explicitly to plugins array AFTER TypeScript preset processes declare fields
                exclude: ["@babel/plugin-transform-class-properties"],
            },
        ],
        // IMPORTANT: Babel processes presets in REVERSE order (last to first)
        // So TypeScript preset (LAST in array) runs FIRST
        // This ensures TypeScript processes declare fields before any class-related plugins run
        [
            "@babel/preset-typescript",
            {
                allowDeclareFields: true,
                allowNamespaces: true,
                isTSX: true, // ✅ TSX parsing için kritik - TypeScript private keyword'lerini parse edebilmek için
                allExtensions: true, // ✅ isTSX:true kullanıldığında zorunlu - tüm dosya uzantılarını TypeScript olarak işle
            },
        ],
    ],
    plugins: [
        // CRITICAL: Add TypeScript plugin explicitly BEFORE class-properties to ensure declare fields are transformed
        // Even though TypeScript preset runs first (because it's last in presets array), we need to ensure
        // that the TypeScript plugin specifically removes declare fields before class-properties plugin runs
        // NOTE: isTSX and allExtensions are NOT valid options for the plugin - they're only for the preset
        [
            "@babel/plugin-transform-typescript",
            {
                allowDeclareFields: true,
                allowNamespaces: true,
            },
        ],
        
        "@babel/plugin-proposal-export-default-from",
        "@babel/plugin-transform-numeric-separator",
        "@babel/plugin-transform-object-rest-spread",
        "@babel/plugin-transform-optional-chaining",
        "@babel/plugin-transform-nullish-coalescing-operator",

        // transform logical assignment (??=, ||=, &&=). preset-env doesn't
        // normally bother with these (presumably because all the target
        // browsers support it natively), but they make our webpack version (or
        // something downstream of babel, at least) fall over.
        "@babel/plugin-transform-logical-assignment-operators",

        "@babel/plugin-syntax-dynamic-import",
        "@babel/plugin-transform-runtime",
        
        // Class-related plugins - MUST run AFTER @babel/plugin-transform-typescript
        // Order is critical: class-properties -> private-methods -> private-property-in-object -> decorators
        "@babel/plugin-transform-class-properties", // Must run AFTER TypeScript plugin processes declare fields
        "@babel/plugin-transform-private-methods", // required for TypeScript private methods
        "@babel/plugin-transform-private-property-in-object", // required for TypeScript private fields
        
        ["@babel/plugin-proposal-decorators", { version: "2023-11" }], // only needed by the js-sdk
        "@babel/plugin-transform-class-static-block", // only needed by the js-sdk for decorators
    ],
};
