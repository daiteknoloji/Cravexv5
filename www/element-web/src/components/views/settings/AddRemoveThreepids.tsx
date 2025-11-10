/*
Copyright 2024 New Vector Ltd.
Copyright 2024 The Matrix.org Foundation C.I.C.

SPDX-License-Identifier: AGPL-3.0-only OR GPL-3.0-only OR LicenseRef-Element-Commercial
Please see LICENSE files in the repository root for full details.
*/

import React, { useCallback, useRef, useState } from "react";
import { logger } from "matrix-js-sdk/src/logger";
import {
    MatrixError,
    ThreepidMedium,
} from "matrix-js-sdk/src/matrix";

import AddThreepid, { type Binding, type ThirdPartyIdentifier } from "../../../AddThreepid";
import { _t, UserFriendlyError } from "../../../languageHandler";
import AccessibleButton, { type ButtonEvent } from "../elements/AccessibleButton";
import { useMatrixClientContext } from "../../../contexts/MatrixClientContext";
import Modal from "../../../Modal";
import ErrorDialog, { extractErrorMessageFromError } from "../dialogs/ErrorDialog";
import Field from "../elements/Field";
import { looksValid as emailLooksValid } from "../../../email";
import CountryDropdown from "../auth/CountryDropdown";
import { type PhoneNumberCountryDefinition } from "../../../phonenumber";
import InlineSpinner from "../elements/InlineSpinner";

// Whether we're adding 3pids to the user's account on the homeserver or sharing them on an identity server
type TheepidControlMode = "hs" | "is";

interface ExistingThreepidProps {
    mode: TheepidControlMode;
    threepid: ThirdPartyIdentifier;
    onChange: (threepid: ThirdPartyIdentifier) => void;
    disabled?: boolean;
}

const ExistingThreepid: React.FC<ExistingThreepidProps> = ({ mode, threepid, onChange, disabled }) => {
    const [isConfirming, setIsConfirming] = useState(false);
    const client = useMatrixClientContext();
    const bindTask = useRef<AddThreepid>(undefined);

    const [isVerifyingBind, setIsVerifyingBind] = useState(false);
    const [continueDisabled, setContinueDisabled] = useState(false);
    const [verificationCode, setVerificationCode] = useState("");

    const onRemoveClick = useCallback((e: ButtonEvent) => {
        e.stopPropagation();
        e.preventDefault();

        setIsConfirming(true);
    }, []);

    const onCancelClick = useCallback((e: ButtonEvent) => {
        e.stopPropagation();
        e.preventDefault();

        setIsConfirming(false);
    }, []);

    const onConfirmRemoveClick = useCallback(
        (e: ButtonEvent) => {
            e.stopPropagation();
            e.preventDefault();

            client
                .deleteThreePid(threepid.medium, threepid.address)
                .then(() => {
                    return onChange(threepid);
                })
                .catch((err) => {
                    logger.error("Unable to remove contact information: " + err);
                    Modal.createDialog(ErrorDialog, {
                        title: _t("settings|general|error_remove_3pid"),
                        description: err?.message ?? _t("invite|failed_generic"),
                    });
                });
        },
        [client, threepid, onChange],
    );

    const changeBinding = useCallback(
        async ({ bind, label, errorTitle }: Binding) => {
            try {
                if (bind) {
                    bindTask.current = new AddThreepid(client);
                    setContinueDisabled(true);
                    if (threepid.medium === ThreepidMedium.Email) {
                        await bindTask.current.bindEmailAddress(threepid.address);
                    } else {
                        // XXX: Sydent will accept a number without country code if you add
                        // a leading plus sign to a number in E.164 format (which the 3PID
                        // address is), but this goes against the spec.
                        // See https://github.com/matrix-org/matrix-doc/issues/2222
                        await bindTask.current.bindMsisdn(null as unknown as string, `+${threepid.address}`);
                    }
                    setContinueDisabled(false);
                    setIsVerifyingBind(true);
                } else {
                    await client.unbindThreePid(threepid.medium, threepid.address);
                    onChange(threepid);
                }
            } catch (err) {
                logger.error(`changeBinding: Unable to ${label} email address ${threepid.address}`, err);
                setIsVerifyingBind(false);
                setContinueDisabled(false);
                bindTask.current = undefined;
                Modal.createDialog(ErrorDialog, {
                    title: errorTitle,
                    description: extractErrorMessageFromError(err, _t("invite|failed_generic")),
                });
            }
        },
        [client, threepid, onChange],
    );

    const onRevokeClick = useCallback(
        (e: ButtonEvent): void => {
            e.stopPropagation();
            e.preventDefault();
            changeBinding({
                bind: false,
                label: "revoke",
                errorTitle:
                    threepid.medium === "email"
                        ? _t("settings|general|error_revoke_email_discovery")
                        : _t("settings|general|error_revoke_msisdn_discovery"),
            }).then();
        },
        [changeBinding, threepid.medium],
    );

    const onShareClick = useCallback(
        (e: ButtonEvent): void => {
            e.stopPropagation();
            e.preventDefault();
            changeBinding({
                bind: true,
                label: "share",
                errorTitle:
                    threepid.medium === "email"
                        ? _t("settings|general|error_share_email_discovery")
                        : _t("settings|general|error_share_msisdn_discovery"),
            }).then();
        },
        [changeBinding, threepid.medium],
    );

    const onContinueClick = useCallback(
        async (e: ButtonEvent) => {
            e.stopPropagation();
            e.preventDefault();

            setContinueDisabled(true);
            try {
                if (threepid.medium === ThreepidMedium.Email) {
                    await bindTask.current?.checkEmailLinkClicked();
                } else {
                    await bindTask.current?.haveMsisdnToken(verificationCode);
                }
                setIsVerifyingBind(false);
                onChange(threepid);
                bindTask.current = undefined;
            } catch (err) {
                logger.error(`Unable to verify threepid:`, err);

                let underlyingError = err;
                if (err instanceof UserFriendlyError) {
                    underlyingError = err.cause;
                }

                if (underlyingError instanceof MatrixError && underlyingError.errcode === "M_THREEPID_AUTH_FAILED") {
                    Modal.createDialog(ErrorDialog, {
                        title:
                            threepid.medium === "email"
                                ? _t("settings|general|email_not_verified")
                                : _t("settings|general|error_msisdn_verification"),
                        description:
                            threepid.medium === "email"
                                ? _t("settings|general|email_verification_instructions")
                                : extractErrorMessageFromError(err, _t("invite|failed_generic")),
                    });
                } else {
                    logger.error("Unable to verify email address: " + err);
                    Modal.createDialog(ErrorDialog, {
                        title: _t("settings|general|error_email_verification"),
                        description: extractErrorMessageFromError(err, _t("invite|failed_generic")),
                    });
                }
            } finally {
                setContinueDisabled(false);
            }
        },
        [verificationCode, onChange, threepid],
    );

    const onVerificationCodeChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        setVerificationCode(e.target.value);
    }, []);

    if (isConfirming) {
        return (
            <div className="mx_AddRemoveThreepids_existing">
                <span className="mx_AddRemoveThreepids_existing_promptText">
                    {threepid.medium === ThreepidMedium.Email
                        ? _t("settings|general|remove_email_prompt", { email: threepid.address })
                        : _t("settings|general|remove_msisdn_prompt", { phone: threepid.address })}
                </span>
                <AccessibleButton
                    onClick={onConfirmRemoveClick}
                    kind="danger_sm"
                    className="mx_AddRemoveThreepids_existing_button"
                >
                    {_t("action|remove")}
                </AccessibleButton>
                <AccessibleButton
                    onClick={onCancelClick}
                    kind="link_sm"
                    className="mx_AddRemoveThreepids_existing_button"
                >
                    {_t("action|cancel")}
                </AccessibleButton>
            </div>
        );
    }

    if (isVerifyingBind) {
        if (threepid.medium === ThreepidMedium.Email) {
            return (
                <div className="mx_EmailAddressesPhoneNumbers_verify">
                    <span className="mx_EmailAddressesPhoneNumbers_verify_instructions">
                        {_t("settings|general|discovery_email_verification_instructions")}
                    </span>
                    <AccessibleButton
                        className="mx_EmailAddressesPhoneNumbers_existing_button"
                        kind="primary_sm"
                        onClick={onContinueClick}
                        disabled={continueDisabled}
                    >
                        {_t("action|complete")}
                    </AccessibleButton>
                </div>
            );
        } else {
            return (
                <div className="mx_EmailAddressesPhoneNumbers_verify">
                    <span className="mx_EmailAddressesPhoneNumbers_verify_instructions">
                        {_t("settings|general|msisdn_verification_instructions")}
                    </span>
                    <form onSubmit={onContinueClick} autoComplete="off" noValidate={true}>
                        <Field
                            type="text"
                            label={_t("settings|general|msisdn_verification_field_label")}
                            autoComplete="off"
                            disabled={continueDisabled}
                            value={verificationCode}
                            onChange={onVerificationCodeChange}
                        />
                    </form>
                </div>
            );
        }
    }

    return (
        <div className="mx_AddRemoveThreepids_existing">
            <span className="mx_AddRemoveThreepids_existing_address">{threepid.address}</span>
            <AccessibleButton
                onClick={mode === "hs" ? onRemoveClick : threepid.bound ? onRevokeClick : onShareClick}
                kind={mode === "hs" || threepid.bound ? "danger_sm" : "primary_sm"}
                disabled={disabled}
            >
                {mode === "hs" ? _t("action|remove") : threepid.bound ? _t("action|revoke") : _t("action|share")}
            </AccessibleButton>
        </div>
    );
};

const AddThreepidSection: React.FC<{ medium: "email" | "msisdn"; disabled?: boolean; onChange: () => void }> = ({
    medium,
    disabled,
    onChange,
}) => {
    const [newThreepidInput, setNewThreepidInput] = useState("");
    const [phoneCountryInput, setPhoneCountryInput] = useState("");
    const [continueDisabled, setContinueDisabled] = useState(false);

    const client = useMatrixClientContext();

    const onPhoneCountryChanged = useCallback((country: PhoneNumberCountryDefinition) => {
        setPhoneCountryInput(country.iso2);
    }, []);

    const onNewThreepidInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        setNewThreepidInput(e.target.value);
    }, []);

    const onAddClick = useCallback(
        async (e: React.FormEvent) => {
            e.stopPropagation();
            e.preventDefault();

            if (!newThreepidInput) return;

            // TODO: Inline field validation
            if (medium === "email" && !emailLooksValid(newThreepidInput)) {
                Modal.createDialog(ErrorDialog, {
                    title: _t("settings|general|error_invalid_email"),
                    description: _t("settings|general|error_invalid_email_detail"),
                });
                return;
            }

            // SADECE: Admin panel API'sini kullan (SMTP YOK - direkt database'e kaydet)
            setContinueDisabled(true);
            
            try {
                const userId = client.getUserId();
                if (!userId) {
                    throw new Error("Kullanıcı ID bulunamadı");
                }
                
                // Admin panel URL'ini homeserver'dan türet
                const homeserverUrl = client.getHomeserverUrl();
                let adminPanelUrl: string;
                
                if (homeserverUrl.includes('matrix-synapse.up.railway.app')) {
                    adminPanelUrl = 'https://considerate-adaptation-production.up.railway.app';
                } else if (homeserverUrl.includes('localhost') || homeserverUrl.includes('127.0.0.1')) {
                    adminPanelUrl = homeserverUrl.replace('/_matrix', '').replace(':8008', ':9000');
                } else {
                    adminPanelUrl = homeserverUrl.replace('/_matrix', '').replace(':8008', ':9000');
                }
                
                const addressToSave = medium === "email" 
                    ? newThreepidInput 
                    : `${phoneCountryInput}${newThreepidInput}`;
                
                logger.log(`[AddThreepid] Admin panel API çağrısı: ${adminPanelUrl}/api/users/${encodeURIComponent(userId)}/threepid`);
                
                const response = await fetch(`${adminPanelUrl}/api/users/${encodeURIComponent(userId)}/threepid`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        medium: medium === "email" ? "email" : "msisdn",
                        address: addressToSave
                    })
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    // Başarılı - direkt database'e kaydedildi
                    setContinueDisabled(false);
                    setNewThreepidInput(""); // Input'u temizle
                    onChange(); // Refresh threepids list
                    
                    // Başarı mesajı göster
                    Modal.createDialog(ErrorDialog, {
                        title: medium === "email" ? "E-posta Eklendi" : "Telefon Eklendi",
                        description: `${medium === "email" ? "E-posta" : "Telefon"} adresi başarıyla kaydedildi.`,
                    });
                    return;
                } else {
                    // API hatası
                    throw new Error(result.error || `API hatası: ${response.status}`);
                }
            } catch (error) {
                logger.error(`[AddThreepid] Admin panel API hatası:`, error);
                setContinueDisabled(false);
                
                // Hata mesajını göster
                Modal.createDialog(ErrorDialog, {
                    title: medium === "email" ? "E-posta Eklenemedi" : "Telefon Eklenemedi",
                    description: error instanceof Error 
                        ? error.message 
                        : `${medium === "email" ? "E-posta" : "Telefon"} adresi kaydedilemedi. Lütfen tekrar deneyin.`,
                });
            }
        },
        [client, phoneCountryInput, newThreepidInput, medium, onChange],
    );

    // SMTP doğrulama modalı kaldırıldı - artık direkt database'e kaydediyoruz
    // Loading state için continueDisabled kullanılıyor

    const phoneCountry =
        medium === "msisdn" ? (
            <CountryDropdown
                onOptionChange={onPhoneCountryChanged}
                className="mx_PhoneNumbers_country"
                value={phoneCountryInput}
                disabled={continueDisabled}
                isSmall={true}
                showPrefix={true}
            />
        ) : undefined;

    return (
        <form onSubmit={onAddClick} autoComplete="off" noValidate={true}>
            <Field
                type="text"
                label={
                    medium === "email"
                        ? _t("settings|general|email_address_label")
                        : _t("settings|general|msisdn_label")
                }
                autoComplete={medium === "email" ? "email" : "tel-national"}
                disabled={disabled || continueDisabled}
                value={newThreepidInput}
                onChange={onNewThreepidInputChange}
                prefixComponent={phoneCountry}
            />
            <AccessibleButton onClick={onAddClick} kind="primary" disabled={disabled || continueDisabled}>
                {continueDisabled ? "Ekleniyor..." : _t("action|add")}
            </AccessibleButton>
        </form>
    );
};

interface AddRemoveThreepidsProps {
    // Whether the control is for adding 3pids to the user's homeserver account or sharing them on an IS
    mode: TheepidControlMode;
    // Whether the control is for emails or phone numbers
    medium: ThreepidMedium;
    // The current list of third party identifiers
    threepids: ThirdPartyIdentifier[];
    // If true, the component is disabled and no third party identifiers can be added or removed
    disabled?: boolean;
    // Called when changes are made to the list of third party identifiers
    onChange: () => void;
    // If true, a spinner is shown instead of the component
    isLoading: boolean;
}

export const AddRemoveThreepids: React.FC<AddRemoveThreepidsProps> = ({
    mode,
    medium,
    threepids,
    disabled,
    onChange,
    isLoading,
}) => {
    if (isLoading) {
        return <InlineSpinner />;
    }

    const existingEmailElements = threepids.map((e) => {
        return <ExistingThreepid mode={mode} threepid={e} onChange={onChange} key={e.address} disabled={disabled} />;
    });

    return (
        <>
            {existingEmailElements}
            {mode === "hs" && <AddThreepidSection medium={medium} disabled={disabled} onChange={onChange} />}
        </>
    );
};
