# pylint: disable=super-with-arguments
# pylint:disable=too-many-lines
from __future__ import (
    annotations,
)

from collections.abc import (
    Iterable,
    Sequence,
)
from decimal import (
    Decimal,
)


class CustomBaseException(Exception):
    pass


class _SingleMessageException(CustomBaseException):
    msg: str

    @classmethod
    def new(cls) -> _SingleMessageException:
        return cls(cls.msg)


class EnrollmentUserExists(_SingleMessageException):
    msg: str = "Enrollment user already exists"


class ErrorFileNameAlreadyExists(_SingleMessageException):
    msg: str = "File name already exists in group files"


class ExecutionAlreadyCreated(_SingleMessageException):
    msg: str = "This execution has already exists"


class ErrorDownloadingFile(_SingleMessageException):
    msg: str = "Unable to download the requested file"


class ErrorLoadingOrganizations(_SingleMessageException):
    msg: str = "Unable to read organizations data"


class ErrorLoadingStakeholders(_SingleMessageException):
    msg: str = "Unable to read stakeholders data"


class ErrorSubmittingJob(_SingleMessageException):
    msg: str = "Unable to queue machine execution or job"


class ErrorSubscribingStakeholder(_SingleMessageException):
    msg: str = "Unable to subscribe stakeholder"


class ErrorUpdatingCredential(_SingleMessageException):
    msg: str = "Unable to update credential"


class ErrorUpdatingGroup(_SingleMessageException):
    msg: str = "Unable to update group"


class ErrorUploadingFileS3(_SingleMessageException):
    msg: str = "Unable to upload file to S3 service"


class ExpectedVulnToBeOfLinesType(_SingleMessageException):
    msg: str = "Expected vulnerability to be of type: lines"


class EventAlreadyCreated(_SingleMessageException):
    msg: str = "This event has already been created"


class GroupAlreadyCreated(_SingleMessageException):
    msg: str = "This group has already been created"


class IndicatorAlreadyUpdated(CustomBaseException):
    """Exception to control the indicator has not been updated"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The indicator has been updated by another operation"
        super(IndicatorAlreadyUpdated, self).__init__(msg)


class InvalidSeverityCweIds(_SingleMessageException):
    msg = "Exception - Error invalid CWE ids given for vulnerability"


class InvalidCVSS3VectorString(_SingleMessageException):
    msg = "Exception - Error invalid severity CVSS v3.1 vector string"


class InvalidGroupName(_SingleMessageException):
    msg = "Exception - Error invalid group name"


class InvalidInactivityPeriod(_SingleMessageException):
    msg = (
        "Exception - Inactivity period should be greater than "
        "the provided value"
    )


class InvalidRemovalVulnState(_SingleMessageException):
    msg: str = "Invalid, you cannot remove a closed vulnerability"


class InvalidSortsParameters(_SingleMessageException):
    msg: str = "Invalid, missing parameters in mutation"


class InvalidSortsSuggestions(_SingleMessageException):
    msg: str = "Invalid, incorrect parameters in ToE Lines Sorts suggestions"


class InvalidSortsRiskLevel(_SingleMessageException):
    msg: str = "Invalid, value not in range [0, 100]"


class InvalidSortsRiskLevelDate(_SingleMessageException):
    msg: str = "Invalid, date can not be a future date."


class InvalidVulnerabilityAlreadyExists(_SingleMessageException):
    msg: str = "Invalid, vulnerability already exists"


class InvalidVulnCommitHash(_SingleMessageException):
    msg: str = "Commit Hash should be a 40 chars long hexadecimal"


class InvalidVulnSpecific(_SingleMessageException):
    msg: str = "Vulnerability Specific must be integer"


class InvalidVulnWhere(_SingleMessageException):
    msg: str = "Vulnerability where should match: ^(?!=)+[^/]+/.+$"


class OrganizationAlreadyCreated(_SingleMessageException):
    msg: str = "This organization has already been created"


class OrgFindingPolicyNotFound(_SingleMessageException):
    msg: str = "Organization finding policy not found"


class PortfolioNotFound(_SingleMessageException):
    msg: str = "Portfolio not found"


class SnapshotNotFound(_SingleMessageException):
    msg: str = "Snapshot not found in analytics bucket"


class UnableToSkimsQueue(_SingleMessageException):
    msg: str = "Unable to queue a verification request"


class UnableToSendMail(_SingleMessageException):
    msg: str = "Unable to send mail message"


class UnavailabilityError(_SingleMessageException):
    msg: str = "AWS service unavailable, please retry"


class VulnAlreadyCreated(_SingleMessageException):
    msg: str = "This vulnerability has already been created"


class AcceptanceNotRequested(CustomBaseException):
    """Exception to control if acceptance is not valid"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - It cant handle acceptance without being requested"
        super(AcceptanceNotRequested, self).__init__(msg)


class HasRejectedDrafts(CustomBaseException):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - User has pending rejected drafts"
        super(HasRejectedDrafts, self).__init__(msg)


class AlreadyApproved(CustomBaseException):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been approved"
        super(AlreadyApproved, self).__init__(msg)


class AlreadyCreated(CustomBaseException):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been created"
        super(AlreadyCreated, self).__init__(msg)


class AlreadyPendingDeletion(CustomBaseException):
    """Exception to control pending to delete groups"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This group has already been deleted or is pending"
        super(AlreadyPendingDeletion, self).__init__(msg)


class AlreadyRequested(CustomBaseException):
    """Exception to control verifications already requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Request verification already requested"
        super(AlreadyRequested, self).__init__(msg)


class AlreadyOnHold(CustomBaseException):
    """Exception to control requested verifications already put on hold"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Request verification already on hold"
        super(AlreadyOnHold, self).__init__(msg)


class AlreadySubmitted(CustomBaseException):
    """Exception to control submitted drafts"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been submitted"
        super(AlreadySubmitted, self).__init__(msg)


class AlreadyZeroRiskRequested(CustomBaseException):
    """Exception to control zero risk already is already requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Zero risk vulnerability is already requested"
        super(AlreadyZeroRiskRequested, self).__init__(msg)


class AlreadyZeroRiskConfirmed(CustomBaseException):
    """Exception to control uploaded vulns that were already flagged as ZR"""

    def __init__(self, info: str = "") -> None:
        """Constructor"""
        if info:
            msg = (
                "Exception - Uploaded vulnerability is a confirmed Zero "
                f"Risk: {info}"
            )
        else:
            msg = "Exception - Uploaded vulnerability is a confirmed Zero Risk"
        super(AlreadyZeroRiskConfirmed, self).__init__(msg)


class DocumentNotFound(CustomBaseException):
    """Exception to control analytics data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Document not found"
        super(DocumentNotFound, self).__init__(msg)


class DraftWithoutVulns(CustomBaseException):
    """Exception to control draft approval process"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "CANT_APPROVE_FINDING_WITHOUT_VULNS"
        super(DraftWithoutVulns, self).__init__(msg)


class DuplicateDraftFound(CustomBaseException):
    """Exception to control duplicates in the draft creation process"""

    def __init__(self, kind: str) -> None:
        """Constructor"""
        msg = (
            f"Exception - A {kind} of this type has been already created."
            " Please submit vulnerabilities there"
        )
        super(DuplicateDraftFound, self).__init__(msg)


class EmptyPoolName(CustomBaseException):
    """Exception to control an empty pool of groups name"""

    def __init__(self, entity: str) -> None:
        """Constructor"""
        msg = (
            f"Exception - There are no {entity} names available at the moment"
        )
        super(EmptyPoolName, self).__init__(msg)


class EventAlreadyClosed(CustomBaseException):
    """Exception to control event updates"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The event has already been closed"
        super(EventAlreadyClosed, self).__init__(msg)


class EventNotFound(CustomBaseException):
    """Exception to control event data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Event not found"
        super(EventNotFound, self).__init__(msg)


class EvidenceNotFound(CustomBaseException):
    """Exception to control evidence data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Evidence not found"
        super(EvidenceNotFound, self).__init__(msg)


class ExpiredToken(CustomBaseException):
    """Exception to control if an user token exists, so has not expired"""

    def __init__(self) -> None:
        msg = "Exception - User token has expired"
        super(ExpiredToken, self).__init__(msg)


class InvalidAlgorithm(CustomBaseException):
    """Exception to control and handle cases where an unsupported or
    invalid algorithm is used to sign or verify a JWT token."""

    def __init__(self) -> None:
        msg = "Invalid algorithm used in the JWT token."
        super(InvalidAlgorithm, self).__init__(msg)


class FileInfected(CustomBaseException):
    """Exception if an uploaded file is infected"""

    def __init__(self) -> None:
        msg = "Exception - File infected"
        super(FileInfected, self).__init__(msg)


class FindingNotFound(CustomBaseException):
    """Exception to control finding data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied"
        super(FindingNotFound, self).__init__(msg)


class GroupNameNotFound(CustomBaseException):
    """Exception to control if the group name has been found."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Group name has not been found"
        super(GroupNameNotFound, self).__init__(msg)


class EnrollmentNotFound(CustomBaseException):
    """Exception to control enrollment availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or enrollment not found"
        super(EnrollmentNotFound, self).__init__(msg)


class GroupNotFound(CustomBaseException):
    """Exception to control group availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or group not found"
        super(GroupNotFound, self).__init__(msg)


class HasVulns(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A root with reported vulns can't be updated"
        super(HasVulns, self).__init__(msg)


class IncompleteDraft(CustomBaseException):
    """Exception to control draft submission"""

    def __init__(self, fields: Sequence[str]) -> None:
        """Constructor"""
        msg = f'Exception - This draft has missing fields: {", ".join(fields)}'
        super(IncompleteDraft, self).__init__(msg)


class IncompleteFinding(CustomBaseException):
    def __init__(self, fields: Sequence[str]) -> None:
        """Constructor"""
        msg = (
            f'Exception - This finding has missing fields: {", ".join(fields)}'
        )
        super(IncompleteFinding, self).__init__(msg)


class IncompleteSeverity(CustomBaseException):
    """Exception to control severity fields"""

    def __init__(self, fields: Iterable[str]) -> None:
        """Constructor"""
        msg = f'Exception - Severity has missing fields: {", ".join(fields)}'
        super(IncompleteSeverity, self).__init__(msg)


class InvalidAcceptanceDays(CustomBaseException):
    """Exception to control correct input in organization settings"""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Exception - {expr}"
        else:
            msg = "Exception - Acceptance days should be a positive integer"
        super(InvalidAcceptanceDays, self).__init__(msg)


class InvalidMinTimeToRemediate(CustomBaseException):
    """Exception to control correct MTTR input in draft creation"""

    def __init__(self) -> None:
        msg = "Exception - Min time to remediate should be a positive number"
        super(InvalidMinTimeToRemediate, self).__init__(msg)


class InvalidAcceptanceSeverity(CustomBaseException):
    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = (
                "Exception - Vulnerability cannot be accepted, severity "
                "outside of range set by the defined policy"
            )
        else:
            msg = (
                "Exception - Severity value must be a positive "
                "floating number between 0.0 and 10.0"
            )
        super(InvalidAcceptanceSeverity, self).__init__(msg)


class InvalidAcceptanceSeverityRange(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Min acceptance severity value should not "
            "be higher than the max value"
        )
        super(InvalidAcceptanceSeverityRange, self).__init__(msg)


class InvalidVulnerabilityGracePeriod(CustomBaseException):
    """Exception to control correct input in organization settings
    (DevSecOps vulnerability grace period)"""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Exception - {expr}"
        else:
            msg = (
                "Exception - Vulnerability grace period value should be a "
                "positive integer"
            )
        super(InvalidVulnerabilityGracePeriod, self).__init__(msg)


class InvalidAuthorization(CustomBaseException):
    """Exception to control authorization."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid Authorization"
        super(InvalidAuthorization, self).__init__(msg)


class InvalidChar(CustomBaseException):
    """Exception to control invalid characters in forms"""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Exception - Invalid characters in {expr}"
        else:
            msg = "Exception - Invalid characters"
        super(InvalidChar, self).__init__(msg)


class InvalidBePresentFilterCursor(CustomBaseException):
    """Exception to control the be present filter cursor"""

    def __init__(self) -> None:
        msg = (
            "Exception - The cursor is invalid for the value in "
            "the be present filter"
        )
        super(InvalidBePresentFilterCursor, self).__init__(msg)


class InvalidFilter(CustomBaseException):
    """Exception to control the supported filters"""

    def __init__(self, filter_name: str) -> None:
        msg = f"Exception - The filter is not supported: {filter_name}"
        super(InvalidFilter, self).__init__(msg)


class InvalidFilterCursor(CustomBaseException):
    """Exception to control the cursor with filters"""

    def __init__(self) -> None:
        msg = "Exception - The cursor is invalid with a filter"
        super(InvalidFilterCursor, self).__init__(msg)


class InvalidCommentParent(CustomBaseException):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Comment parent is invalid"
        super(InvalidCommentParent, self).__init__(msg)


class InvalidSpacesField(CustomBaseException):
    """Exception to avoid fields from being filled with spaces."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Field cannot fill with blank characters"
        super(InvalidSpacesField, self).__init__(msg)


class MachineCouldNotBeQueued(CustomBaseException):
    """Exception to handle when a Machine job cannot be queued"""

    def __init__(self) -> None:
        msg: str = (
            "Exception - Machine execution could not be queued. "
            "Either the group has the service disabled "
            "or the roots specified are invalid"
        )
        super(MachineCouldNotBeQueued, self).__init__(msg)


class MachineExecutionAlreadySubmitted(CustomBaseException):
    """Exception to handle when a Machine job cannot be queued
    due to an existing one"""

    def __init__(self) -> None:
        msg: str = (
            "Exception - There is already a Machine execution queued "
            "with the same parameters"
        )
        super(MachineExecutionAlreadySubmitted, self).__init__(msg)


class RepeatedComment(CustomBaseException):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Comment already exists "
        super(RepeatedComment, self).__init__(msg)


class InvalidCVSSField(CustomBaseException):
    """Exception to control CVSS field values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - CVSS field value must be a number"
        super(InvalidCVSSField, self).__init__(msg)


class InvalidCVSSVersion(CustomBaseException):
    """Exception to control CVSS version"""

    def __init__(self) -> None:
        """Constructor"""
        msg: str = "Invalid, CVSS version is not supported"
        super(InvalidCVSSVersion, self).__init__(msg)


class InvalidDate(CustomBaseException):
    """Exception to control the date inserted in an Accepted vulnerability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The inserted date is invalid"
        super(InvalidDate, self).__init__(msg)


class InvalidDateFormat(CustomBaseException):
    """Exception to control the date format inserted in an Accepted
    vulnerability and the API deprecation notices"""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        if expr:
            msg = f"Exception - The date format is invalid: {expr}"
        else:
            msg = "Exception - The date format is invalid"
        super(InvalidDateFormat, self).__init__(msg)


class InvalidDraftConsult(CustomBaseException):
    """Exception to halt consults made in drafts"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Consults are not allowed in Drafts"
        super(InvalidDraftConsult, self).__init__(msg)


class InvalidExpirationTime(CustomBaseException):
    """Exception to control valid expiration time."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid Expiration Time"
        super(InvalidExpirationTime, self).__init__(msg)


class TokenCouldNotBeAdded(CustomBaseException):
    """Exception to control number of added tokens."""

    def __init__(self) -> None:
        """Constructor"""
        msg = (
            "Exception - Could not add token, maximum number"
            " of tokens at the same time is 2"
        )
        super(TokenCouldNotBeAdded, self).__init__(msg)


class TokenNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Access denied or token not found"
        super(TokenNotFound, self).__init__(msg)


class InvalidField(CustomBaseException):
    """Exception to control invalid fields in forms"""

    def __init__(self, field: str = "field") -> None:
        """Constructor"""
        msg = f"Exception - Invalid {field} in form"
        super(InvalidField, self).__init__(msg)


class InvalidFieldLength(CustomBaseException):
    """Exception to control invalid field length in forms"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid field length in form"
        super(InvalidFieldLength, self).__init__(msg)


class InvalidFileSize(CustomBaseException):
    """Exception to control file size."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid file size"
        super(InvalidFileSize, self).__init__(msg)


class InvalidFileStructure(CustomBaseException):
    """Exception to control file structure."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Wrong file structure"
        super(InvalidFileStructure, self).__init__(msg)


class InvalidFileType(CustomBaseException):
    """Exception to control file type."""

    def __init__(self, detail: str = "") -> None:
        """Constructor"""
        msg = "Exception - Invalid file type"
        if detail:
            msg += f": {detail}"
        super(InvalidFileType, self).__init__(msg)


class InvalidFileName(CustomBaseException):
    """Exception to control type filename."""

    def __init__(self, detail: str = "") -> None:
        """Constructor"""
        msg = "Exception - Invalid file name"
        if detail:
            msg += f": {detail}"
        super(InvalidFileName, self).__init__(msg)


class InvalidFindingTitle(CustomBaseException):
    """Exception to control draft and finding titles"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The inserted Draft/Finding title is invalid"
        super(InvalidFindingTitle, self).__init__(msg)


class InvalidFieldChange(CustomBaseException):
    """Exception to control forbidden field changes"""

    def __init__(self, fields: Sequence[str], reason: str) -> None:
        """Constructor"""
        msg = (
            f'Exception - Forbidden change on field: {", ".join(fields)}'
            f"  Reason: {reason}"
        )
        super(InvalidFieldChange, self).__init__(msg)


class InvalidGroupServicesConfig(CustomBaseException):
    """Exception to control that services attached to a group are valid."""

    def __init__(self, msg: str) -> None:
        """Constructor"""
        super(InvalidGroupServicesConfig, self).__init__(f"Exception - {msg}")


class InvalidGroupTier(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Invalid tier. "
            "Only 'oneshot', 'machine', 'squad' and 'free' allowed."
        )
        super(InvalidGroupTier, self).__init__(msg)


class InvalidJustificationMaxLength(CustomBaseException):
    """Exception to control justification length"""

    def __init__(self, field: int) -> None:
        """Constructor"""
        msg = (
            "Exception - Justification must have a maximum of "
            f"{field} characters"
        )
        super(InvalidJustificationMaxLength, self).__init__(msg)


class InvalidMarkdown(CustomBaseException):
    """Exception to control invalid markdown fields"""

    def __init__(self) -> None:
        msg = "Exception - Invalid markdown"
        super(InvalidMarkdown, self).__init__(msg)


class InvalidNotificationRequest(CustomBaseException):
    """Exception to control invalid email notification requests"""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Exception - Invalid email notification request: {expr}"
        else:
            msg = "Exception - Invalid email notification request"
        super(InvalidNotificationRequest, self).__init__(msg)


class InvalidNumberAcceptances(CustomBaseException):
    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = (
                "Exception - Vulnerability has been accepted the maximum "
                "number of times allowed by the defined policy"
            )
        else:
            msg = (
                "Exception - Number of acceptances should be zero or positive"
            )
        super(InvalidNumberAcceptances, self).__init__(msg)


class InvalidOrganization(CustomBaseException):
    """Exception to prevent repeated organizations"""

    def __init__(self, msg: str = "") -> None:
        """Constructor"""
        if msg == "":
            msg = "Access denied"
        super(InvalidOrganization, self).__init__(msg)


class InvalidParameter(CustomBaseException):
    """Exception to control empty required parameters"""

    def __init__(self, field: str = "") -> None:
        """Constructor"""
        if field:
            msg = f"Exception - Field {field} is invalid"
        else:
            msg = "Exception - Error value is not valid"
        super(InvalidParameter, self).__init__(msg)


class InvalidPath(CustomBaseException):
    """Exception to control valid path value in vulnerabilities."""

    def __init__(self, expr: str) -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in path value", {expr}}}'
        super(InvalidPath, self).__init__(msg)


class InvalidPort(CustomBaseException):
    """Exception to control valid port value in vulnerabilities."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in port value", {expr}}}'
        super(InvalidPort, self).__init__(msg)


class InvalidPositiveArgument(CustomBaseException):
    def __init__(self, arg: str) -> None:
        """Constructor"""
        msg = f"The argument must be a positive integer: {arg}"
        super(InvalidPositiveArgument, self).__init__(f"Exception - {msg}")


class InvalidRange(CustomBaseException):
    """Exception to control valid range in vulnerabilities."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in range limit numbers", {expr}}}'
        super(InvalidRange, self).__init__(msg)


class InvalidRoleProvided(CustomBaseException):
    """Exception to control that users only grant roles they're allowed to."""

    def __init__(self, role: str) -> None:
        """Constructor"""
        msg = f"Invalid role or not enough permissions to grant role: {role}"
        super(InvalidRoleProvided, self).__init__(f"Exception - {msg}")


class InvalidRootComponent(CustomBaseException):
    """Exception to control the root has the component"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The root does not have the component"
        super(InvalidRootComponent, self).__init__(msg)


class InvalidIpAddressInRoot(CustomBaseException):
    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The root does not have the IP address"
        super(InvalidIpAddressInRoot, self).__init__(msg)


class InvalidRootExclusion(CustomBaseException):
    """Exception to control exclusion paths"""

    def __init__(self) -> None:
        """Constructor"""
        msg = (
            "Exception - Root name should not be included in the exception "
            "pattern"
        )
        super(InvalidRootExclusion, self).__init__(msg)


class InvalidSchema(CustomBaseException):
    """Exception to control schema validation."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Invalid Schema", {expr}}}'
        super(InvalidSchema, self).__init__(msg)


class InvalidSeverity(CustomBaseException):
    """Exception to control severity value"""

    def __init__(self, fields: Sequence[Decimal]) -> None:
        """Constructor"""
        msg = (
            "Exception - Severity value must be between "
            f"{fields[0]} and {fields[1]}"
        )
        super(InvalidSeverity, self).__init__(msg)


class InvalidReportFilter(CustomBaseException):
    """Exception to control severity value"""

    def __init__(self, expr: str = "") -> None:
        msg: str = "Exception - Invalid filter"
        if expr:
            msg = f"Exception - {expr}"
        super(InvalidReportFilter, self).__init__(msg)


class InvalidSeverityUpdateValues(CustomBaseException):
    """Exception to control severity update values"""

    def __init__(self) -> None:
        """Constructor"""
        msg: str = "Invalid, severity update values out of range"
        super(InvalidSeverityUpdateValues, self).__init__(msg)


class InvalidSource(CustomBaseException):
    """Exception to control if the source is valid."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid source"
        super(InvalidSource, self).__init__(msg)


class InvalidStream(CustomBaseException):
    """Exception to control stream validation."""

    def __init__(self, vuln_type: str = "", index: str = "") -> None:
        """Constructor"""
        msg = (
            '{"msg": "Exception - Invalid stream should start \'home\' or '
            f'\'query\'", "path": "/{vuln_type}/{index}"}}'
        )
        super(InvalidStream, self).__init__(msg)


class InvalidStateStatus(CustomBaseException):
    """Exception to control state status."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid state status"
        super(InvalidStateStatus, self).__init__(msg)


class InvalidAssigned(CustomBaseException):
    """Exception to control if assigned user is valid"""

    def __init__(self) -> None:
        msg = "Assigned not valid"
        super(InvalidAssigned, self).__init__(msg)


class InvalidUserProvided(CustomBaseException):
    """Exception to control that users belong to Fluid Attacks before they're
    granted a restricted role"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "This role can only be granted to Fluid Attacks users"
        super(InvalidUserProvided, self).__init__(f"Exception - {msg}")


class InvalidVulnsNumber(CustomBaseException):
    """Exception to control number of vulnerabilities provided to upload."""

    def __init__(self, number_of_vulns: int = 100) -> None:
        msg = (
            "Exception - You can upload a maximum of "
            f"{number_of_vulns} vulnerabilities per file"
        )
        super(InvalidVulnsNumber, self).__init__(msg)


class NotVerificationRequested(CustomBaseException):
    """Exception to control finding verification"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Error verification not requested"
        super(NotVerificationRequested, self).__init__(msg)


class NotSubmitted(CustomBaseException):
    """Exception to control unsubmitted drafts"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The draft has not been submitted yet"
        super(NotSubmitted, self).__init__(msg)


class NotZeroRiskRequested(CustomBaseException):
    """Exception to control zero risk already is not requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Zero risk vulnerability is not requested"
        super(NotZeroRiskRequested, self).__init__(msg)


class OrganizationNotFound(CustomBaseException):
    """Exception to control organization availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or organization not found"
        super(OrganizationNotFound, self).__init__(msg)


class PermissionDenied(CustomBaseException):
    """Exception to control permission"""

    def __init__(self) -> None:
        msg = "Exception - Error permission denied"
        super(PermissionDenied, self).__init__(msg)


class RepeatedRoot(CustomBaseException):
    """Exception to prevent repeated roots"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Root with the same URL/branch already exists"
        super(RepeatedRoot, self).__init__(msg)


class RepeatedRootNickname(CustomBaseException):
    """Exception to prevent repeated roots"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Root with the same nickname already exists"
        super(RepeatedRootNickname, self).__init__(msg)


class RepeatedToeInput(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe input already exists"
        super(RepeatedToeInput, self).__init__(msg)


class RepeatedToeLines(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe lines already exists"
        super(RepeatedToeLines, self).__init__(msg)


class RepeatedToePort(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe port already exists"
        super(RepeatedToePort, self).__init__(msg)


class RepeatedValues(CustomBaseException):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - One or more values already exist"
        super(RepeatedValues, self).__init__(msg)


class RequestedInvitationTooSoon(CustomBaseException):
    """Exception to control that new invitations to the same user in the same
    group/org are spaced out by at least one minute"""

    def __init__(self) -> None:
        """Constructor"""
        msg = (
            "The previous invitation to this user was requested less"
            " than a minute ago"
        )
        super(RequestedInvitationTooSoon, self).__init__(f"Exception - {msg}")


class RequestedReportError(CustomBaseException):
    """Exception to control cert, pdf, xls or data report error."""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Error - {expr}"
        else:
            msg = "Error - Some error ocurred generating the report"
        super(RequestedReportError, self).__init__(msg)


class ReportAlreadyRequested(CustomBaseException):
    def __init__(self) -> None:
        msg: str = (
            "Exception - The user already has a requested report "
            "for the same group"
        )
        super(ReportAlreadyRequested, self).__init__(msg)


class CredentialNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Access denied or credential not found"
        super(CredentialNotFound, self).__init__(msg)


class RootNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Access denied or root not found"
        super(RootNotFound, self).__init__(msg)


class RootEnvironmentUrlNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Access denied or root environment url not found"
        super(RootEnvironmentUrlNotFound, self).__init__(msg)


class SameValues(CustomBaseException):
    """Exception to control save values updating treatment"""

    def __init__(self) -> None:
        msg = "Exception - Same values"
        super(SameValues, self).__init__(msg)


class SecureAccessException(CustomBaseException):
    """Exception that controls access to resources with authentication."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Access to resources without active session"
        super(SecureAccessException, self).__init__(msg)


class StakeholderHasGroupAccess(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The stakeholder has been granted access to "
            "the group previously"
        )
        super(StakeholderHasGroupAccess, self).__init__(msg)


class StakeholderHasOrganizationAccess(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The stakeholder has been granted access to "
            "the organization previously"
        )
        super(StakeholderHasOrganizationAccess, self).__init__(msg)


class StakeholderNotFound(CustomBaseException):
    """Exception to control stakeholder availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or stakeholder not found"
        super(StakeholderNotFound, self).__init__(msg)


class TagNotFound(CustomBaseException):
    """Exception to control tag availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or tag not found"
        super(TagNotFound, self).__init__(msg)


class ToeInputAlreadyUpdated(CustomBaseException):
    """Exception to control the toe input has not been updated"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The toe input has been updated by another operation"
        super(ToeInputAlreadyUpdated, self).__init__(msg)


class ToeInputNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe input has not been found"
        super(ToeInputNotFound, self).__init__(msg)


class ToeLinesAlreadyUpdated(CustomBaseException):
    """Exception to control the toe lines has not been updated"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The toe lines has been updated by another operation"
        super(ToeLinesAlreadyUpdated, self).__init__(msg)


class ToeLinesNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe lines has not been found"
        super(ToeLinesNotFound, self).__init__(msg)


class ToePortAlreadyUpdated(CustomBaseException):
    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The toe port has been updated by another operation"
        super(ToePortAlreadyUpdated, self).__init__(msg)


class ToePortNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe port has not been found"
        super(ToePortNotFound, self).__init__(msg)


class UnexpectedUserRole(CustomBaseException):
    """Exception to control that roles attached to an user are valid."""

    def __init__(self, msg: str) -> None:
        """Constructor"""
        super(UnexpectedUserRole, self).__init__(f"Exception - {msg}")


class UserNotFound(CustomBaseException):
    """Exception to control user data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - User not found"
        super(UserNotFound, self).__init__(msg)


class StakeholderNotInOrganization(CustomBaseException):
    """
    Exception to control stakeholder access to organizations.
    """

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = "Exception - Stakeholder is not a member of the organization"
        else:
            msg = "Access denied"
        super(StakeholderNotInOrganization, self).__init__(msg)


class StakeholderNotInGroup(CustomBaseException):
    """
    Exception to control stakeholder access to groups.
    """

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = "Exception - Stakeholder is not a member of the group"
        else:
            msg = "Access denied"
        super(StakeholderNotInGroup, self).__init__(msg)


class ExecutionNotFound(CustomBaseException):
    """
    Exception to control data availability.
    """

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = "Exception - Execution not found"
        else:
            msg = "Access denied"
        super(ExecutionNotFound, self).__init__(msg)


class VulnAlreadyClosed(CustomBaseException):
    """Exception to control vulnerability updates"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The vulnerability has already been closed"
        super(VulnAlreadyClosed, self).__init__(msg)


class VulnNotFound(CustomBaseException):
    """Exception to control vulnerability data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Vulnerability not found"
        super(VulnNotFound, self).__init__(msg)


class VulnNotInFinding(CustomBaseException):
    """
    Exception to control vulnerability in finding
    """

    def __init__(self) -> None:
        msg = "Exception - Vulnerability does not belong to finding"
        super(VulnNotInFinding, self).__init__(msg)


class InvalidFindingNamePolicy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The finding name is invalid"
        super(InvalidFindingNamePolicy, self).__init__(msg)


class RepeatedFindingNamePolicy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The finding name policy already exists"
        super(RepeatedFindingNamePolicy, self).__init__(msg)


class PolicyAlreadyHandled(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - This policy has already been reviewed"
        super(PolicyAlreadyHandled, self).__init__(msg)


class MachineCanNotOperate(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Machine cannot operate at this time"
        super(MachineCanNotOperate, self).__init__(msg)


class InactiveRoot(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The root is not active"
        super(InactiveRoot, self).__init__(msg)


class RootAlreadyCloning(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The root already has an active cloning process"
        super(RootAlreadyCloning, self).__init__(msg)


class ToeInputNotPresent(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The toe input is not present"
        super(ToeInputNotPresent, self).__init__(msg)


class InvalidToeInputAttackedAt(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The attack time must be between the previous "
            "attack and the current time"
        )
        super(InvalidToeInputAttackedAt, self).__init__(msg)


class InvalidToeInputAttackedBy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The input attacked by attribute is mandatory"
        super(InvalidToeInputAttackedBy, self).__init__(msg)


class InvalidToeLinesAttackAt(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The attack time must be between the previous "
            "attack and the current time"
        )
        super(InvalidToeLinesAttackAt, self).__init__(msg)


class InvalidToeLinesAttackedLines(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The attacked lines must be between 0 and the loc "
            "(lines of code)"
        )
        super(InvalidToeLinesAttackedLines, self).__init__(msg)


class ToePortNotPresent(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The toe port is not present"
        super(ToePortNotPresent, self).__init__(msg)


class InvalidToePortAttackedAt(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The attack time must be between the previous "
            "attack and the current time"
        )
        super(InvalidToePortAttackedAt, self).__init__(msg)


class InvalidToePortAttackedBy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The port attacked by attribute is mandatory"
        super(InvalidToePortAttackedBy, self).__init__(msg)


class InvalidBillingCustomer(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Cannot perform action. "
            "Please add a valid payment method first"
        )
        super(InvalidBillingCustomer, self).__init__(msg)


class NoActiveBillingSubscription(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - There is not an active subscription for this group"
        super(NoActiveBillingSubscription, self).__init__(msg)


class NumberOutOfRange(CustomBaseException):
    def __init__(
        self, lower_bound: int, upper_bound: int, inclusive: bool
    ) -> None:
        inclusive_str = " (inclusive)" if inclusive else ""
        msg = (
            f"Exception - Value must be between {lower_bound}{inclusive_str} "
            f"and {upper_bound}{inclusive_str}"
        )
        super(NumberOutOfRange, self).__init__(msg)


class BillingSubscriptionSameActive(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Invalid subscription. "
            "Provided subscription is already active"
        )
        super(BillingSubscriptionSameActive, self).__init__(msg)


class BillingCustomerHasNoPaymentMethod(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Invalid customer. "
            "Provided customer does not have a payment method"
        )
        super(BillingCustomerHasNoPaymentMethod, self).__init__(msg)


class BillingCustomerHasActiveSubscription(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Cannot perform action. "
            "The organization has active or trialing subscriptions"
        )
        super(BillingCustomerHasActiveSubscription, self).__init__(msg)


class InvalidBillingPaymentMethod(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Invalid payment method. "
            "Provided payment method does not exist for this organization"
        )
        super(InvalidBillingPaymentMethod, self).__init__(msg)


class InvalidExpiryDateField(CustomBaseException):
    """Exception to control expiry credit card date field values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Expiriy month or year field value must be a number"
        super(InvalidExpiryDateField, self).__init__(msg)


class InvalidPaymentBusinessName(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Payment method business name must be match with "
            "group business name"
        )

        super(InvalidPaymentBusinessName, self).__init__(msg)


class CouldNotUpdateSubscription(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Subscription could not be updated, "
            "please review your invoices"
        )
        super(CouldNotUpdateSubscription, self).__init__(msg)


class CouldNotDowngradeSubscription(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Subscription could not be downgraded, "
            "payment intent for Squad failed"
        )
        super(CouldNotDowngradeSubscription, self).__init__(msg)


class CouldNotCreatePaymentMethod(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Provided payment method could not be created"
        super(CouldNotCreatePaymentMethod, self).__init__(msg)


class PaymentMethodAlreadyExists(CustomBaseException):
    def __init__(self) -> None:
        msg: str = (
            "Exception - Provided payment method already exists. "
            "Please update or delete it first"
        )
        super(PaymentMethodAlreadyExists, self).__init__(msg)


class InvalidManagedChange(CustomBaseException):
    def __init__(self) -> None:
        msg: str = (
            "Exception - Incorrect change in managed parameter. "
            "Please review the payment conditions"
        )
        super(InvalidManagedChange, self).__init__(msg)


class InvalidGitCredentials(CustomBaseException):
    def __init__(self) -> None:
        msg: str = (
            "Exception - Git repository was not accessible "
            "with given credentials"
        )
        super(InvalidGitCredentials, self).__init__(msg)


class OutdatedRepository(CustomBaseException):
    def __init__(self) -> None:
        msg: str = "Exception - The git repository is outdated"
        super(OutdatedRepository, self).__init__(msg)


class EmptyHistoric(CustomBaseException):
    """Exception to control the historic is not empty"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The historic can not be empty"
        super(EmptyHistoric, self).__init__(msg)


class InvalidUrl(CustomBaseException):
    """Exception to control the url is valid"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The URL is not valid"
        super(InvalidUrl, self).__init__(msg)


class CouldNotStartStakeholderVerification(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Stakeholder verification could not be started"
        super(CouldNotStartStakeholderVerification, self).__init__(msg)


class CouldNotVerifyStakeholder(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Stakeholder could not be verified"
        super(CouldNotVerifyStakeholder, self).__init__(msg)


class InvalidVerificationCode(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The verification code is invalid"
        super(InvalidVerificationCode, self).__init__(msg)


class InvalidMobileNumber(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - A mobile number is required with the "
            "international format"
        )
        super(InvalidMobileNumber, self).__init__(msg)


class RequiredVerificationCode(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The verification code is required"
        super(RequiredVerificationCode, self).__init__(msg)


class RequiredNewPhoneNumber(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A new phone number is required"
        super(RequiredNewPhoneNumber, self).__init__(msg)


class SamePhoneNumber(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The new phone number is the current phone number"
        super(SamePhoneNumber, self).__init__(msg)


class VulnerabilityPathDoesNotExistInToeLines(CustomBaseException):
    def __init__(self, index: str = "") -> None:
        msg = (
            '{"msg": "Exception - The vulnerability path does not exist in '
            f'the toe lines", "path": "/lines/{index}"}}'
        )
        super(VulnerabilityPathDoesNotExistInToeLines, self).__init__(msg)


class VulnerabilityUrlFieldDoNotExistInToeInputs(CustomBaseException):
    def __init__(self, index: str = "") -> None:
        msg = (
            '{"msg": "Exception -  The vulnerability URL and field do not '
            f'exist in the toe inputs", "path": "/inputs/{index}"}}'
        )
        super(VulnerabilityUrlFieldDoNotExistInToeInputs, self).__init__(msg)


class VulnerabilityPortFieldDoNotExistInToePorts(CustomBaseException):
    def __init__(self, index: str = "") -> None:
        msg = (
            '{"msg": "Exception -  The vulnerability address and port do not '
            f'exist in the toe ports", "path": "/ports/{index}"}}'
        )
        super(VulnerabilityPortFieldDoNotExistInToePorts, self).__init__(msg)


class LineDoesNotExistInTheLinesOfCodeRange(CustomBaseException):
    def __init__(self, line: str, index: str) -> None:
        msg = (
            '{"msg": "Exception -  The line does not exist in the range '
            f'of 0 and lines of code: {line}", "path": "/lines/{index}"}}'
        )
        super(LineDoesNotExistInTheLinesOfCodeRange, self).__init__(msg)


class VulnerabilityEntryNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Vulnerability entry not found"
        super(VulnerabilityEntryNotFound, self).__init__(msg)


class RequiredStateStatus(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - State status is required"
        super(RequiredStateStatus, self).__init__(msg)


class UnsanitizedInputFound(CustomBaseException):
    """Exception to control unsanitized input"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Unsanitized input found"
        super(UnsanitizedInputFound, self).__init__(msg)


class InvalidCommitHash(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The commit hash is invalid"
        super(InvalidCommitHash, self).__init__(msg)


class InvalidGitRoot(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A git root is required"
        super(InvalidGitRoot, self).__init__(msg)


class InvalidModifiedDate(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The modified date can not be a future date"
        super(InvalidModifiedDate, self).__init__(msg)


class InvalidLinesOfCode(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Lines of code must be equal or greater than 0"
        super(InvalidLinesOfCode, self).__init__(msg)


class CredentialAlreadyExists(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A credential exists with the same name"
        super(CredentialAlreadyExists, self).__init__(msg)


class RequiredCredentials(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Credentials is required"
        super(RequiredCredentials, self).__init__(msg)


class OnlyCorporateEmails(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Only corporate emails are allowed"
        super(OnlyCorporateEmails, self).__init__(msg)


class InvalidCredentialSecret(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Invalid secret for the credential type"
        super(InvalidCredentialSecret, self).__init__(msg)


class RepeatedCredential(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Credential already exists"
        super(RepeatedCredential, self).__init__(msg)


class InvalidBase64SshKey(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The ssh key must be in base64"
        super(InvalidBase64SshKey, self).__init__(msg)


class UnableToSendSms(CustomBaseException):
    def __init__(self) -> None:
        msg: str = "Exception - Unable to send sms message"
        super(UnableToSendSms, self).__init__(msg)


class EventHasNotBeenSolved(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The event has not been solved"
        super(EventHasNotBeenSolved, self).__init__(msg)


class BranchNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Branch not found"
        super(BranchNotFound, self).__init__(msg)


class RequiredFieldToBeUpdate(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A field is required to be updated"
        super(RequiredFieldToBeUpdate, self).__init__(msg)


class EventVerificationAlreadyRequested(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The event verification has been requested"
        super(EventVerificationAlreadyRequested, self).__init__(msg)


class EventVerificationNotRequested(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The event verification has not been requested"
        super(EventVerificationNotRequested, self).__init__(msg)


class TooManyRequests(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Too many requests"
        super(TooManyRequests, self).__init__(msg)


class InvalidRootType(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The type of the root is invalid"
        super(InvalidRootType, self).__init__(msg)


class FileNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The file has not been found"
        super(FileNotFound, self).__init__(msg)


class InvalidEventSolvingReason(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The solving reason is not valid for the event type"
        super(InvalidEventSolvingReason, self).__init__(msg)


class TrialRestriction(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The action is not allowed during the free trial"
        super(TrialRestriction, self).__init__(msg)


class GroupHasPendingActions(CustomBaseException):
    def __init__(self, action_names: list[str]) -> None:
        msg = f"Exception - The group has pending actions: {str(action_names)}"
        super(GroupHasPendingActions, self).__init__(msg)


class VulnerabilityHasNotBeenReleased(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The vulnerability has not been released"
        super(VulnerabilityHasNotBeenReleased, self).__init__(msg)


class VulnerabilityHasNotBeenRejected(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The vulnerability has not been rejected"
        super(VulnerabilityHasNotBeenRejected, self).__init__(msg)


class VulnerabilityHasNotBeenSubmitted(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The vulnerability has not been submitted"
        super(VulnerabilityHasNotBeenSubmitted, self).__init__(msg)


class InvalidStandardId(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The standard id is invalid"
        super(InvalidStandardId, self).__init__(msg)


class InvalidVulnerabilityRequirement(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The requirement is not valid in the vulnerability"
        super(InvalidVulnerabilityRequirement, self).__init__(msg)


class RepeatedFindingThreat(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Finding with the same threat already exists"
        super(RepeatedFindingThreat, self).__init__(msg)


class RepeatedFindingDescription(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Finding with the same description already exists"
        super(RepeatedFindingDescription, self).__init__(msg)


class RequiredUnfulfilledRequirements(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The unfulfilled requirements are required"
        super(RequiredUnfulfilledRequirements, self).__init__(msg)


class RepeatedFindingMachineDescription(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Finding with the same description, threat and"
            " severity already exists"
        )
        super(RepeatedFindingMachineDescription, self).__init__(msg)


class InvalidSeverityScore(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Severity score is invalid"
        super(InvalidSeverityScore, self).__init__(msg)


class RequiredSubmittedStatus(CustomBaseException):
    def __init__(self, where: str, specific: str) -> None:
        msg = (
            '{"msg": "Exception - New vulnerabilities require the submitted'
            f' status", "where": "{where}", "specific": "{specific}" }}'
        )
        super(RequiredSubmittedStatus, self).__init__(msg)


class VulnerabilityCantNotChangeStatus(CustomBaseException):
    def __init__(self, where: str, specific: str, status: str) -> None:
        msg = (
            '{"msg": "Exception - Uploaded vulnerability can not change the'
            f' status", "status": "{status}", "where": "{where}", "specific":'
            f' "{specific}" }}'
        )

        super(VulnerabilityCantNotChangeStatus, self).__init__(msg)


class InvalidNewVulnStateStatus(_SingleMessageException):
    def __init__(self, status: str) -> None:
        msg = (
            f"Invalid, only New vulnerabilities with {status} state are"
            " allowed"
        )
        super(InvalidNewVulnStateStatus, self).__init__(msg)


class RequiredRemovalReason(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The removal reason is required"
        super(RequiredRemovalReason, self).__init__(msg)


class InvalidFilterAccess(CustomBaseException):
    def __init__(self, filter_name: str) -> None:
        msg = f"Exception - The filter is not available: {filter_name}"
        super(InvalidFilterAccess, self).__init__(msg)
