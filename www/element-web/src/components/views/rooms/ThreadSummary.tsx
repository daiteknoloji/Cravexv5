/*
Copyright 2024 New Vector Ltd.
Copyright 2022 The Matrix.org Foundation C.I.C.

SPDX-License-Identifier: AGPL-3.0-only OR GPL-3.0-only OR LicenseRef-Element-Commercial
Please see LICENSE files in the repository root for full details.
*/

import React, { useContext, useMemo } from "react";
import type { HTMLAttributes, JSX } from "react";
import { type Thread, ThreadEvent, type MatrixEvent, THREAD_RELATION_TYPE } from "matrix-js-sdk/src/matrix";
import { IndicatorIcon } from "@vector-im/compound-web";
import ThreadIconSolid from "@vector-im/compound-design-tokens/assets/web/icons/threads-solid";

import { _t } from "../../../languageHandler";
import { CardContext } from "../right_panel/context";
import AccessibleButton, { type ButtonEvent } from "../elements/AccessibleButton";
import PosthogTrackers from "../../../PosthogTrackers";
import { useTypedEventEmitterState } from "../../../hooks/useEventEmitter";
import MemberAvatar from "../avatars/MemberAvatar";
import { Action } from "../../../dispatcher/actions";
import { type ShowThreadPayload } from "../../../dispatcher/payloads/ShowThreadPayload";
import defaultDispatcher from "../../../dispatcher/dispatcher";
import { useUnreadNotifications } from "../../../hooks/useUnreadNotifications";
import { notificationLevelToIndicator } from "../../../utils/notifications";
import { EventPreviewTile, useEventPreview } from "./EventPreview.tsx";
import { useScopedRoomContext } from "../../../contexts/ScopedRoomContext.tsx";

interface IProps extends HTMLAttributes<HTMLDivElement> {
    mxEvent: MatrixEvent;
    thread: Thread;
}

const ThreadSummary: React.FC<IProps> = ({ mxEvent, thread, ...props }) => {
    const cardContext = useContext(CardContext);
    const roomContext = useScopedRoomContext("narrow");
    const totalCount = useTypedEventEmitterState(thread, ThreadEvent.Update, () => thread.length) ?? 0;
    const events = useTypedEventEmitterState(thread, ThreadEvent.Update, () => thread.events?.slice() ?? []);
    const replies = useMemo(
        () => {
            const unique = new Map<string, MatrixEvent>();
            for (const event of events) {
                const key = event.getId() ?? event.getTxnId() ?? `pending-${event.getTs()}`;
                unique.set(key, event);
            }

            return Array.from(unique.values())
                .filter(
                    (event) =>
                        event.getId() !== mxEvent.getId() &&
                        THREAD_RELATION_TYPE.names.some((name) => event.isRelation(name)),
                )
                .slice(-5);
        },
        [events, mxEvent],
    );
    const { level } = useUnreadNotifications(thread.room, thread.id);

    const onOpenThread = (ev: ButtonEvent): void => {
        defaultDispatcher.dispatch<ShowThreadPayload>({
            action: Action.ShowThread,
            rootEvent: mxEvent,
            push: cardContext.isCard,
        });
        PosthogTrackers.trackInteraction("WebRoomTimelineThreadSummaryButton", ev);
    };

    if (roomContext.narrow) {
        if (!totalCount) return null;
        return (
            <AccessibleButton
                {...props}
                className="mx_ThreadSummary"
                onClick={onOpenThread}
                aria-label={_t("custom_thread|open_panel")}
            >
                <IndicatorIcon size="24px" indicator={notificationLevelToIndicator(level)}>
                    <ThreadIconSolid />
                </IndicatorIcon>
                <span className="mx_ThreadSummary_replies_amount">{totalCount}</span>
                <ThreadMessagePreview thread={thread} showDisplayname={false} />
                <div className="mx_ThreadSummary_chevron" />
            </AccessibleButton>
        );
    }

    if (!replies.length) return null;

    return (
        <div {...props} className="mx_ThreadSummaryInline">
            <div className="mx_ThreadSummaryInline_header">
                <IndicatorIcon size="24px" indicator={notificationLevelToIndicator(level)}>
                    <ThreadIconSolid />
                </IndicatorIcon>
                <span className="mx_ThreadSummaryInline_label">
                    {_t("custom_thread|header", { count: replies.length })}
                </span>
                <AccessibleButton className="mx_ThreadSummaryInline_openButton" onClick={onOpenThread}>
                    {_t("custom_thread|open_panel")}
                </AccessibleButton>
            </div>
            <ol className="mx_ThreadSummaryInline_list">
                {replies.map((reply) => (
                    <li
                        key={reply.getId() ?? reply.getTxnId() ?? `pending-${reply.getTs()}`}
                        className="mx_ThreadSummaryInline_item"
                    >
                        <ThreadReplyItem mxEvent={reply} showDisplayname={!roomContext.narrow} />
                    </li>
                ))}
            </ol>
        </div>
    );
};

interface IPreviewProps {
    thread: Thread;
    showDisplayname?: boolean;
}

export const ThreadMessagePreview: React.FC<IPreviewProps> = ({ thread, showDisplayname = false }) => {
    const lastReply = useTypedEventEmitterState(thread, ThreadEvent.Update, () => thread.replyToEvent) ?? undefined;
    const preview = useEventPreview(lastReply);

    if (!preview || !lastReply) {
        return null;
    }

    return (
        <>
            <MemberAvatar
                member={lastReply.sender}
                fallbackUserId={lastReply.getSender()}
                size="24px"
                className="mx_ThreadSummary_avatar"
            />
            {showDisplayname && (
                <div className="mx_ThreadSummary_sender">{lastReply.sender?.name ?? lastReply.getSender()}</div>
            )}

            {lastReply.isDecryptionFailure() ? (
                <div
                    className="mx_ThreadSummary_content mx_DecryptionFailureBody"
                    title={_t("timeline|decryption_failure|unable_to_decrypt")}
                >
                    {_t("timeline|decryption_failure|unable_to_decrypt")}
                </div>
            ) : (
                <EventPreviewTile preview={preview} className="mx_ThreadSummary_content" />
            )}
        </>
    );
};

interface ThreadReplyItemProps {
    mxEvent: MatrixEvent;
    showDisplayname: boolean;
}

const ThreadReplyItem: React.FC<ThreadReplyItemProps> = ({ mxEvent, showDisplayname }): JSX.Element => {
    const preview = useEventPreview(mxEvent);

    return (
        <div className="mx_ThreadSummary_reply">
            <MemberAvatar
                member={mxEvent.sender}
                fallbackUserId={mxEvent.getSender()}
                size="24px"
                className="mx_ThreadSummary_avatar"
            />
            <div className="mx_ThreadSummary_replyBody">
                {showDisplayname && (
                    <div className="mx_ThreadSummary_replySender">{mxEvent.sender?.name ?? mxEvent.getSender()}</div>
                )}

                {mxEvent.isDecryptionFailure() ? (
                    <div
                        className="mx_ThreadSummary_replyText mx_DecryptionFailureBody"
                        title={_t("timeline|decryption_failure|unable_to_decrypt")}
                    >
                        {_t("timeline|decryption_failure|unable_to_decrypt")}
                    </div>
                ) : preview ? (
                    <EventPreviewTile preview={preview} className="mx_ThreadSummary_replyText" />
                ) : (
                    <span className="mx_ThreadSummary_replyFallback">{_t("custom_thread|reply_fallback")}</span>
                )}
            </div>
        </div>
    );
};

export default ThreadSummary;
