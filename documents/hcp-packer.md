# HCP Packer Service Principal and Team Access Guide

## Overview

This document provides guidance on implementing service principals and team access for HashiCorp Cloud Platform (HCP) Packer within our organization. It covers the business rationale, security considerations, and step-by-step implementation procedures.

## What is HCP Packer?

HCP Packer is HashiCorp's managed service for tracking and managing machine image artifacts across multiple cloud providers and platforms. It provides a centralized registry for golden images, enabling teams to track image lineage, metadata, and deployment status across environments.

## Why Service Principals and Team Access Matter

### Business Justification

**Operational Efficiency**
- Eliminates manual credential management across CI/CD pipelines
- Reduces time spent on access provisioning and troubleshooting
- Enables automated image building and deployment workflows

**Security and Compliance**
- Implements principle of least privilege access
- Provides audit trails for image operations
- Separates human and machine identities
- Supports compliance requirements for infrastructure automation

**Scalability**
- Supports multiple teams and projects without credential conflicts
- Enables self-service access patterns within guardrails
- Facilitates consistent access patterns across environments

### Key Benefits

1. **Automated Workflows**: Service principals enable CI/CD systems to interact with HCP Packer without human intervention
2. **Fine-grained Permissions**: Team-based access controls ensure users only access relevant image artifacts
3. **Auditability**: Clear tracking of who performed what actions on which images
4. **Reduced Risk**: Eliminates shared credentials and reduces exposure of sensitive tokens

## Service Principal Implementation

### When to Use Service Principals

Service principals should be used for:
- CI/CD pipeline integrations
- Automated image building processes
- Infrastructure as Code (IaC) deployments
- Monitoring and alerting systems
- Any non-human system requiring HCP Packer access

### Creating Service Principals

#### Prerequisites
- HCP Organization Admin or Project Admin role
- Access to HCP Console
- Understanding of target use case and required permissions

#### Step-by-Step Process

1. **Navigate to HCP Console**
   - Log into HCP Console
   - Select your organization
   - Navigate to "Access control (IAM)"

2. **Create Service Principal**
   - Click "Service principals" tab
   - Select "Create service principal"
   - Provide descriptive name (e.g., `packer-ci-prod`, `image-builder-dev`)
   - Add description explaining purpose and owner

3. **Generate Credentials**
   - Note the Client ID (this will be needed for authentication)
   - Generate and securely store the Client Secret
   - **Important**: Store credentials in secure credential management system

4. **Assign Permissions**
   - Navigate to project-level IAM
   - Add service principal with appropriate role:
     - `Contributor`: Full read/write access to Packer registries
     - `Viewer`: Read-only access for monitoring/reporting
     - Custom roles: For specific permission requirements

### Service Principal Security Best Practices

**Credential Management**
- Store credentials in dedicated secret management systems (HashiCorp Vault, AWS Secrets Manager, etc.)
- Never commit credentials to version control
- Rotate credentials regularly (recommend quarterly)
- Use different service principals for different environments

**Permission Scoping**
- Apply minimum necessary permissions
- Use project-level assignments when possible
- Regular access reviews and cleanup of unused principals

**Monitoring**
- Enable audit logging for service principal activities
- Set up alerts for unusual access patterns
- Regular review of service principal usage

## Team Access Management

### Access Control Strategy

#### Role-Based Access Control (RBAC)

**Project-Level Roles**
- **Admin**: Full project management including IAM
- **Contributor**: Create, update, and manage Packer registries and images
- **Viewer**: Read-only access to registries and image metadata

#### Team Structure Recommendations

**By Environment**
- `team-packer-prod-contributors`
- `team-packer-staging-contributors`  
- `team-packer-dev-contributors`

**By Application/Product**
- `team-webapp-packer-contributors`
- `team-api-packer-contributors`
- `team-infrastructure-packer-admin`

### Implementing Team Access

#### Setting Up Team-Based Access

1. **Define Team Structure**
   - Map organizational teams to HCP access requirements
   - Determine appropriate permission levels per team
   - Consider environment separation needs

2. **Create Groups (if using external IdP)**
   - Configure groups in your identity provider (AD, Okta, etc.)
   - Map groups to HCP teams during SSO configuration

3. **Assign Team Permissions**
   - Navigate to project IAM settings
   - Add teams/groups with appropriate roles
   - Verify permissions are correctly applied

#### Access Request Workflow

**Standard Process**
1. Team member submits access request via established workflow
2. Team lead/manager approves request
3. Infrastructure team provisions access
4. Access is documented and tracked

**Self-Service Options**
- Consider implementing automated access provisioning for standard roles
- Use infrastructure as code for access management
- Implement time-bound access for temporary needs

## Implementation Examples

### CI/CD Pipeline Integration

```bash
# Environment variables for service principal
export HCP_CLIENT_ID="your-service-principal-client-id"
export HCP_CLIENT_SECRET="your-service-principal-secret"

# Packer build with HCP integration
packer build \
  -var "hcp_packer_registry=myapp" \
  -var "hcp_packer_bucket_name=ubuntu-base" \
  template.pkr.hcl
```

### Terraform Integration

```hcl
# Configure HCP provider with service principal
provider "hcp" {
  client_id     = var.hcp_client_id
  client_secret = var.hcp_client_secret
}

# Reference Packer image in Terraform
data "hcp_packer_image" "ubuntu" {
  bucket_name    = "ubuntu-base"
  channel        = "production"
  cloud_provider = "aws"
  region         = "us-west-2"
}
```

## Governance and Compliance

### Access Review Process

**Monthly Reviews**
- Review active service principals and their usage
- Validate team membership and access levels
- Remove unused or expired access

**Quarterly Audits**
- Comprehensive review of all HCP Packer access
- Validation against organizational changes
- Update documentation and procedures

### Documentation Requirements

**Service Principal Registry**
- Maintain inventory of all service principals
- Document purpose, owner, and expiration dates
- Track credential rotation schedules

**Team Access Matrix**
- Document which teams have access to which projects
- Maintain approval records for access grants
- Regular updates based on organizational changes

## Troubleshooting Common Issues

### Authentication Problems

**Service Principal Authentication Failures**
- Verify client ID and secret are correct
- Check service principal is assigned to correct project
- Confirm service principal has not expired

**Team Access Issues**
- Verify user is member of correct group/team
- Check group mapping in SSO configuration
- Confirm project-level permissions are assigned

### Permission Errors

**Insufficient Permissions**
- Review assigned roles and permissions
- Verify project-level vs organization-level access
- Check for custom role configurations

## Next Steps and Recommendations

### Immediate Actions
1. Audit current HCP Packer access patterns
2. Identify candidates for service principal conversion
3. Design team access structure based on organizational needs
4. Implement secure credential storage solution

### Long-term Improvements
1. Automate access provisioning workflows
2. Implement comprehensive monitoring and alerting
3. Regular security reviews and access certifications
4. Integration with broader identity and access management strategy

## Additional Resources

- [HCP Packer Documentation](https://developer.hashicorp.com/hcp/docs/packer)
- [HCP IAM Documentation](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam)
- [Packer HCP Integration Guide](https://developer.hashicorp.com/packer/tutorials/hcp-get-started)

---

**Document Maintained By**: Infrastructure Team  
**Last Updated**: [Current Date]  
**Review Cycle**: Quarterly