// Prisma schema — mirrors backend SQLAlchemy models for the Next.js layer
// (used for NextAuth session storage, billing, and read-side queries)

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  imageUrl      String?
  plan          Plan      @default(FREE)
  stripeCustomerId String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  projects      Project[]
  subscription  Subscription?
}

enum Plan {
  FREE
  CREATOR
  PRO
  ADMIN
}

model Project {
  id                String    @id @default(cuid())
  userId            String
  user              User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  title             String    @default("Untitled Project")
  videoUrl          String?
  exportedVideoUrl  String?
  status            ProjectStatus @default(QUEUED)
  errorMessage      String?
  durationSeconds   Float?
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt

  segments          CaptionSegment[]
  styleProfile      StyleProfile?

  @@index([userId])
}

enum ProjectStatus {
  QUEUED
  PROCESSING
  COMPLETED
  FAILED
}

model CaptionSegment {
  id            String   @id @default(cuid())
  projectId     String
  project       Project  @relation(fields: [projectId], references: [id], onDelete: Cascade)
  startTime     Float
  endTime       Float
  tamilText     String?
  tanglishText  String
  edited        Boolean  @default(false)
  orderIndex    Int      @default(0)

  @@index([projectId])
}

model StyleProfile {
  id              String   @id @default(cuid())
  projectId       String   @unique
  project         Project  @relation(fields: [projectId], references: [id], onDelete: Cascade)
  fontFamily      String   @default("Poppins")
  fontSize        Int      @default(24)
  position        String   @default("bottom")
  bgOpacity       Float    @default(0.6)
  strokeWidth     Int      @default(2)
  animationPreset String   @default("fade")
}

model Subscription {
  id                 String   @id @default(cuid())
  userId             String   @unique
  user               User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  stripeSubId        String?
  plan               Plan     @default(FREE)
  status             String   @default("active")
  currentPeriodEnd   DateTime?
  createdAt          DateTime @default(now())
}

model UsageStat {
  id                 String   @id @default(cuid())
  userId             String
  minutesProcessed   Float    @default(0)
  videosProcessed    Int      @default(0)
  month              String   // "2026-06"

  @@unique([userId, month])
}
