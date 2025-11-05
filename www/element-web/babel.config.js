module.exports = {
    sourceMaps: true,
    presets: [
        [
            "@babel/preset-typescript",
            {
                allowDeclareFields: true,
                allowNamespaces: true,
            },
        ],
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
        "@babel/preset-react",
    ],
    plugins: [
        // IMPORTANT: Babel processes presets in REVERSE order
        // So @babel/preset-typescript (first in array) runs LAST among presets
        // This ensures TypeScript processes declare fields before plugins run
        // Then class-related plugins must run in this specific order:
        // 1. class-properties (handles regular class fields)
        // 2. private-methods (handles private methods)
        // 3. private-property-in-object (handles private fields)
        // 4. decorators (must run after all class features)
        
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
        
        // Class-related plugins - MUST run AFTER @babel/preset-typescript
        // Order is critical: class-properties -> private-methods -> private-property-in-object -> decorators
        "@babel/plugin-transform-class-properties", // Must run AFTER TypeScript preset processes declare fields
        "@babel/plugin-transform-private-methods", // required for TypeScript private methods
        "@babel/plugin-transform-private-property-in-object", // required for TypeScript private fields
        
        ["@babel/plugin-proposal-decorators", { version: "2023-11" }], // only needed by the js-sdk
        "@babel/plugin-transform-class-static-block", // only needed by the js-sdk for decorators
    ],
};
