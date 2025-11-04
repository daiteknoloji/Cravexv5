/*
Custom help tab for Cravex admin users
*/

import React, { type JSX } from "react";

import { _t } from "../../../../../languageHandler";
import ExternalLink from "../../../elements/ExternalLink";
import SettingsTab from "../SettingsTab";
import { SettingsSection } from "../../shared/SettingsSection";
import { SettingsSubsection, SettingsSubsectionText } from "../../shared/SettingsSubsection";

const HelpUserSettingsTab = (): JSX.Element => (
    <SettingsTab>
        <SettingsSection heading={_t("custom_help|guide_title")}>
            <SettingsSubsection>
                <SettingsSubsectionText>{_t("custom_help|guide_intro")}</SettingsSubsectionText>
                <ol className="mx_HelpUserSettingsTab_list">
                    <li>{_t("custom_help|guide_step_rooms")}</li>
                    <li>{_t("custom_help|guide_step_messages")}</li>
                    <li>{_t("custom_help|guide_step_files")}</li>
                    <li>{_t("custom_help|guide_step_monitoring")}</li>
                </ol>
            </SettingsSubsection>
        </SettingsSection>

        <SettingsSection heading={_t("custom_help|shortcuts_title")}>
            <SettingsSubsection>
                <SettingsSubsectionText>{_t("custom_help|shortcuts_info")}</SettingsSubsectionText>
                <ul className="mx_HelpUserSettingsTab_list">
                    <li>{_t("custom_help|shortcut_navigate")}</li>
                    <li>{_t("custom_help|shortcut_search")}</li>
                    <li>{_t("custom_help|shortcut_settings")}</li>
                </ul>
            </SettingsSubsection>
        </SettingsSection>

        <SettingsSection heading={_t("custom_help|resources_title")}>
            <SettingsSubsection>
                <SettingsSubsectionText>{_t("custom_help|resources_description")}</SettingsSubsectionText>
                <ul className="mx_HelpUserSettingsTab_list">
                    <li>
                        <ExternalLink href="/docs/kullanim-kilavuzu.pdf">
                            {_t("custom_help|resource_manual")}
                        </ExternalLink>
                    </li>
                    <li>
                        <ExternalLink href="/docs/sss.pdf">
                            {_t("custom_help|resource_faq")}
                        </ExternalLink>
                    </li>
                </ul>
            </SettingsSubsection>
        </SettingsSection>

        <SettingsSection heading={_t("custom_help|support_title")}>
            <SettingsSubsection>
                <SettingsSubsectionText>{_t("custom_help|support_description")}</SettingsSubsectionText>
            </SettingsSubsection>
        </SettingsSection>
    </SettingsTab>
);

export default HelpUserSettingsTab;
