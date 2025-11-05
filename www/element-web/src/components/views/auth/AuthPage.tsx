/*
Copyright 2019-2024 New Vector Ltd.
Copyright 2019 The Matrix.org Foundation C.I.C.
Copyright 2015, 2016 OpenMarket Ltd

SPDX-License-Identifier: AGPL-3.0-only OR GPL-3.0-only OR LicenseRef-Element-Commercial
Please see LICENSE files in the repository root for full details.
*/

import React from "react";

import SdkConfig from "../../../SdkConfig";
import AuthFooter from "./AuthFooter";

export default class AuthPage extends React.PureComponent<React.PropsWithChildren> {
    private static welcomeBackgroundUrl?: string | null;

    // cache the url as a static to prevent it changing without refreshing
    private static getWelcomeBackgroundUrl(): string | null {
        if (AuthPage.welcomeBackgroundUrl !== undefined) return AuthPage.welcomeBackgroundUrl || null;

        const brandingConfig = SdkConfig.getObject("branding");
        const configuredUrl = brandingConfig?.get("welcome_background_url");
        
        if (configuredUrl) {
            if (Array.isArray(configuredUrl)) {
                const index = Math.floor(Math.random() * configuredUrl.length);
                AuthPage.welcomeBackgroundUrl = configuredUrl[index] || null;
            } else {
                AuthPage.welcomeBackgroundUrl = configuredUrl || null;
            }
        } else {
            // Boş string veya yoksa null döndür (beyaz arka plan için)
            AuthPage.welcomeBackgroundUrl = null;
        }

        return AuthPage.welcomeBackgroundUrl;
    }

    public render(): React.ReactElement {
        // Beyaz arka plan - welcome_background_url boşsa
        const welcomeBackgroundUrl = AuthPage.getWelcomeBackgroundUrl();
        const pageStyle = welcomeBackgroundUrl
            ? {
                  background: `center/cover fixed url(${welcomeBackgroundUrl})`,
              }
            : {
                  background: "#ffffff",
              };

        const modalStyle: React.CSSProperties = {
            position: "relative",
            background: "initial",
        };

        const blurStyle: React.CSSProperties = welcomeBackgroundUrl
            ? {
                  position: "absolute",
                  top: 0,
                  right: 0,
                  bottom: 0,
                  left: 0,
                  filter: "blur(40px)",
                  background: pageStyle.background,
              }
            : {
                  display: "none",
              };

        const modalContentStyle: React.CSSProperties = {
            display: "flex",
            zIndex: 1,
            background: welcomeBackgroundUrl ? "rgba(255, 255, 255, 0.59)" : "#ffffff",
            borderRadius: "8px",
        };

        return (
            <div className="mx_AuthPage" style={pageStyle}>
                <div className="mx_AuthPage_modal" style={modalStyle}>
                    {welcomeBackgroundUrl && <div className="mx_AuthPage_modalBlur" style={blurStyle} />}
                    <div className="mx_AuthPage_modalContent" style={modalContentStyle}>
                        {this.props.children}
                    </div>
                </div>
                <AuthFooter />
            </div>
        );
    }
}
