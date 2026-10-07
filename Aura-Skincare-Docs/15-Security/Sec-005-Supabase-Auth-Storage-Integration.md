# Supabase Auth & Storage Integration Plan

**Document ID**: SEC-005  
**Title**: Supabase Auth & Storage Integration  
**Status**: Draft  
**Version**: 1.0  
**Owner**: Aura Skincare  
**Date**: 2026-09-23  
**Category**: Infrastructure  

## 1. Overview

This document outlines the plan to integrate Supabase Auth (GoTrue) for authentication management and Supabase Storage (S3-compatible) for file uploads. This replaces the current custom JWT implementation with Supabase's managed auth service and provides scalable file storage for product images, customer avatars, and AI-generated content.

### 1.1 Current State Analysis

**Current Authentication**:
- Custom JWT-based authentication
- Local user management in PostgreSQL
- Email/password, refresh tokens, email verification
- No OAuth providers (Google, GitHub, Apple)
- No built-in MFA support
- Manual token refresh and session management

**Current Storage**:
- Product images, category images, banner images are stored as URLs only
- No actual file upload capability
- Images must be hosted externally
- No CDN integration for global asset delivery
- No signed URL generation for private assets

### 1.2 Goals

1. Migrate authentication to Supabase Auth (GoTrue) for managed identity
2. Enable Supabase Storage for product images, avatars, and AI-generated content
3. Maintain backward compatibility during migration
4. Leverage Supabase's built-in OAuth, MFA, and email templates
5. Reduce custom auth code by ~70%
6. Enable signed URLs for secure private file access

### 1.3 Scope

**In Scope**:
- Supabase Auth integration (signup, login, OAuth, MFA, password reset, email verification)
- Supabase Storage buckets: product-images, customer-avatars, ai-generated, marketing-assets
- Signed URL generation for private assets
- Migration strategy for existing users
- Row Level Security (RLS) policies for data access
- Frontend SDK integration (supabase-js)
- Backend admin client for server-side operations

**Out of Scope**:
- Supabase Realtime subscriptions
- Supabase Edge Functions (keep FastAPI backend)
- Supabase Database branching (keep Alembic migrations)
- Full user data migration in single deployment (phased approach)

### 1.4 Key Decisions

1. **Supabase as Auth Provider**: Use Supabase Auth directly (no token translation layer)
2. **Service Role Key**: Only in backend, never in frontend
3. **RLS Policies**: Primary authorization mechanism for storage
4. **Local User Table**: Keep for business data, linked via supabase_user_id
5. **Phased Migration**: Dual-write period with fallback capability
6. **Image Optimization**: Automatic resize/optimization for uploaded images

### 1.5 Success Metrics

- Auth-related support tickets reduced by 50%
- Custom auth code lines reduced by 70%
- File upload success rate > 99.9%
- Average image load time < 500ms globally
- Zero auth-related security incidents
- 100% OAuth provider functionality (Google, GitHub, Apple)
- CDN cache hit ratio > 95% for public assets

### 1.6 Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Migration complexity for existing users | Phased migration with dual-write period, fallback to legacy auth |
| Token format change (custom JWT vs Supabase JWT) | Update token validation middleware, maintain compatibility layer |
| Storage cost at scale | Lifecycle policies, image optimization, CDN caching |
| Vendor lock-in | S3-compatible API, export tools, portable data format |
| RLS policy misconfiguration | Comprehensive integration tests, staging validation |

## 2. Implementation Plan

### 2.1 Phase 1: Setup & Configuration (Week 1)

1. **Create Supabase Project**:
   - Configure project in Supabase dashboard
   - Set up database connection to existing PostgreSQL
   - Configure storage buckets (product-images, customer-avatars, ai-generated, marketing-assets)
   - Set up environment variables in backend and frontend

2. **Install Dependencies**:
   - Backend: `supabase-py >= 2.0`
   - Frontend: `@supabase/supabase-js >= 2.0`
   - Update dependencies in `backend/requirements.txt` and `frontend/package.json`

3. **Configure Environment Variables**:
   ```env
   # .env.example
   SUPABASE_URL=https://[project-id].supabase.co
   SUPABASE_ANON_KEY=public-anon-key
   SUPABASE_SERVICE_ROLE_KEY=service-role-key
   DATABASE_URL=postgresql+asyncpg://postgres:password@db.[project-id].supabase.co:5432/postgres
   ```

4. **Create Admin Client**:
   - Initialize Supabase client in backend with service role key
   - Create admin endpoints for user management

### 2.2 Phase 2: Auth Migration - New Users Only (Week 2)

1. **Update Registration Flow**:
   - Modify `/register` endpoint to use Supabase Auth API
   - Handle email verification via Supabase
   - Create user record in local database with supabase_user_id

2. **Update Login Flow**:
   - Replace custom login with Supabase Auth API call
   - Receive and validate JWT tokens from Supabase
   - Store user metadata in local database

3. **Add OAuth Providers**:
   - Configure Google, GitHub, Apple providers in Supabase
   - Update login endpoints to support social logins

4. **Enable MFA**:
   - Configure TOTP and SMS options in Supabase
   - Update login flow to support MFA challenges

### 2.3 Phase 3: Storage Integration - Product Images (Week 3)

1. **Create Storage Buckets**:
   - Create 4 buckets: product-images, customer-avatars, ai-generated, marketing-assets
   - Configure bucket policies with RLS
   - Set up signed URL generation for private assets

2. **Update Product Image Service**:
   - Modify `ProductImageService` to use Supabase Storage API
   - Replace URL storage with actual file uploads
   - Implement signed URL generation for secure access

3. **Update API Endpoints**:
   - Modify `/images` endpoints to use Supabase Storage
   - Update response models to include public URLs
   - Implement file type validation and size limits

### 2.4 Phase 4: Storage Integration - Avatars & AI Content (Week 4)

1. **Customer Avatar Storage**:
   - Add avatar upload endpoint in profile routes
   - Implement automatic resize/optimization
   - Update profile display logic to use new avatar URLs

2. **AI-Generated Content Storage**:
   - Update AI tools to upload generated images to Supabase Storage
   - Implement folder structure for AI-generated content
   - Add metadata storage for image descriptions

3. **Marketing Asset Storage**:
   - Create marketing assets bucket
   - Add upload endpoints for banners and campaign images
   - Implement versioning for marketing assets

### 2.5 Phase 5: Existing User Migration (Week 5)

1. **User Data Migration**:
   - Create migration script to map existing users to Supabase Auth
   - Use service role key to update user records
   - Handle edge cases (duplicate emails, inactive accounts)

2. **Dual-Write Period**:
   - Implement dual-write pattern for 2 weeks
   - Write to both old and new auth systems
   - Monitor for consistency issues

3. **Legacy Auth Shutdown**:
   - Decommission custom auth endpoints
   - Remove legacy authentication code
   - Update all references to custom auth

### 2.5 Phase 6: Legacy Auth Cleanup (Week 6)

1. **Remove Custom Auth Code**:
   - Remove all custom auth endpoints and services
   - Remove JWT-related code from backend
   - Remove email verification and password reset endpoints

2. **Cleanup Database**:
   - Remove old auth tables (users, refresh_tokens, etc.)
   - Keep only supabase_user_id in user table
   - Update all foreign key references

3. **Final Validation**:
   - Run comprehensive integration tests
   - Verify all user flows work with Supabase Auth
   - Test storage uploads and downloads
   - Verify RLS policies are correctly configured

## 3. Technical Implementation Details

### 3.1 Authentication Flow

**New User Registration**:
```python
# Backend flow
async def register_user(email: str, password: str, full_name: str):
    # Call Supabase Auth API
    response = await supabase.auth.sign_up(
        email=email,
        password=password
    )
    
    # Verify user exists in Supabase
    if response.user:
        # Create local user record
        user = User(
            supabase_user_id=response.user.id,
            email=email.lower(),
            full_name=full_name,
            role="customer",
            is_active=True,
            is_verified=True  # Assuming email verification is automatic
        )
        await user_repository.create(user)
        return user
```

**Login Flow**:
```python
# Backend flow
async def login_user(email: str, password: str):
    # Call Supabase Auth API
    response = await supabase.auth.sign_in_with_password(
        email=email,
        password=password
    )
    
    if response.user:
        access_token = response.session.access_token
        refresh_token = response.session.refresh_token
        
        # Create local session
        user = await user_repository.get_by_email(email.lower())
        await user_repository.update_last_login(user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
```

### 2.6 Storage Integration Details

**File Upload Process**:
1. Generate signed URL for upload:
```python
# Backend
async def get_upload_url(file_type: str) -> str:
    return await supabase.storage.from('product-images').create_signed_url(
        file_name=f"{uuid4()}.jpg",
        method="PUT",
        expires_in=3600
    )
```

2. **File Upload Process**:
   1. Client requests signed URL
   2. Client uploads file directly to Supabase Storage
   3. Supabase returns file URL
   4. Client stores URL in database or frontend

4. **File Deletion**:
```python
async def delete_image(image_id: uuid.UUID):
    image = await product_image_repository.get_by_id(image_id)
    if image:
        await supabase.storage.from('product-images').remove([image.image_url])
        await product_image_repository.delete(image_id)
```

## 4. Migration Strategy

### 2.6.1 Dual-Write Migration Approach

1. **Phase 1**: Enable both auth systems (legacy + Supabase)
2. **Phase 2**: New users use Supabase Auth only
3. **Phase 3**: Existing users can choose migration path
4. **Phase 7**: Complete migration with legacy auth shutdown

### 2.6.2 Migration Script Outline

```python
# Migration script outline
def migrate_users():
    # Get all users from local database
    users = await user_repository.get_all()
    
    for user in users:
        try:
            # Get user from Supabase
            supabase_user = await supabase.auth.get_user(user.supabase_user_id)
            
            # Update user record
            await user_repository.update(
                user.id,
                supabase_auth_id=response.user.id,
                is_supabase_auth=True
            )
            
        except Exception as e:
            # Handle migration errors
            await log_migration_error(user.id, str(e))
```

## 4. Documentation Requirements

### 4.1 Updated Documentation

1. **API Documentation**:
   - Update API-007 (Authentication) with Supabase Auth endpoints
   - Document new Storage API endpoints for file operations

2. **Developer Documentation**:
   - Create `docs/auth-integration.md` with step-by-step guides
   - Create `docs/storage-integration.md` with file upload examples
   - Update onboarding documentation for new developers

3. **Architecture Diagrams**:
   - Update system architecture diagram to show Supabase integration
   - Add storage flow diagram showing file upload process

### 4.6 Testing Requirements

1. **Unit Tests**:
   - Auth service tests with Supabase mock
   - Storage service tests with mock file uploads
   - Auth middleware tests with JWT validation

2. **Integration Tests**:
   - End-to-end auth flow tests
   - File upload and download tests
   - RLS policy verification tests

3. **Load Testing**:
   - Simulate 1000 concurrent file uploads
   - Test token refresh under load
   - Measure storage API latency

## 5. Rollback Plan

1. **Maintain Legacy Auth**: Keep custom auth system running during migration
2. **Dual-Write**: Write to both systems during migration period
3. **Rollback Points**:
   - Week 2: Rollback new user auth only
   - Week 3: Rollback storage changes only
   - Week 5: Rollback full migration (keep legacy auth)
4. **Monitoring**: Implement detailed logging for all auth and storage operations

## 6. Required Changes

### 5.1 Backend Changes

1. **Add Supabase Client**:
   - Initialize Supabase client in `backend/app/config/supabase.py`
   - Create admin client for server-side operations

2. **Auth Service Updates**:
   - Replace custom auth methods with Supabase API calls
   - Update token validation to use Supabase JWT verification
   - Implement OAuth provider support

3. **Storage Service**:
   - Create `ProductImageService` for Supabase Storage integration
   - Implement signed URL generation and validation
   - Update repository methods to use Storage API

### 5.2 Frontend Changes

1. **Auth Flow**:
   - Update login/register components to use supabase-js
   - Implement OAuth provider buttons
   - Add MFA support flow

2. **File Upload**:
   - Create file upload component for product images
   - Implement drag-and-drop interface
   - Show progress indicator during upload

## 7. Required Resources

- Supabase Project (already created)
- Supabase documentation: https://supabase.com/docs
- supabase-py library documentation
- @supabase/supabase-js documentation
- JWT validation best practices
- RLS policy documentation

## 7. References

- AGENTS.md - Documentation-First Workflow
- API-DOC-001 (API Authentication)
- SEC-002 (Authorization Policy)
- 08-API/authentication.md (Current Auth Implementation)
- FEAT-005.yaml (Feature Specification)
- 15-Security/authentication-policy.md (Security Requirements)