package com.australiarecycling.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "councils")
public class Council {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, unique = true)
  private String slug;

  @Column(nullable = false, length = 10)
  private String state;

  @Column(length = 500)
  private String website;

  @Column(name = "recycling_info_url", length = 500)
  private String recyclingInfoUrl;

  @Column(columnDefinition = "TEXT")
  private String description;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  @Column(name = "updated_at")
  private LocalDateTime updatedAt;

  @OneToMany(mappedBy = "council", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<Suburb> suburbs = new ArrayList<>();

  @OneToMany(mappedBy = "council", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<CouncilMaterial> councilMaterials = new ArrayList<>();

  public Council() {}

  @PrePersist
  protected void onCreate() {
    createdAt = LocalDateTime.now();
    updatedAt = LocalDateTime.now();
  }

  @PreUpdate
  protected void onUpdate() {
    updatedAt = LocalDateTime.now();
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getSlug() {
    return slug;
  }

  public void setSlug(String slug) {
    this.slug = slug;
  }

  public String getState() {
    return state;
  }

  public void setState(String state) {
    this.state = state;
  }

  public String getWebsite() {
    return website;
  }

  public void setWebsite(String website) {
    this.website = website;
  }

  public String getRecyclingInfoUrl() {
    return recyclingInfoUrl;
  }

  public void setRecyclingInfoUrl(String recyclingInfoUrl) {
    this.recyclingInfoUrl = recyclingInfoUrl;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public void setCreatedAt(LocalDateTime createdAt) {
    this.createdAt = createdAt;
  }

  public LocalDateTime getUpdatedAt() {
    return updatedAt;
  }

  public void setUpdatedAt(LocalDateTime updatedAt) {
    this.updatedAt = updatedAt;
  }

  public List<Suburb> getSuburbs() {
    return suburbs;
  }

  public void setSuburbs(List<Suburb> suburbs) {
    this.suburbs = suburbs;
  }

  public List<CouncilMaterial> getCouncilMaterials() {
    return councilMaterials;
  }

  public void setCouncilMaterials(List<CouncilMaterial> councilMaterials) {
    this.councilMaterials = councilMaterials;
  }
}
