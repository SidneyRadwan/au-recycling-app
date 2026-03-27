package com.australiarecycling.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(
    name = "council_materials",
    uniqueConstraints = @UniqueConstraint(columnNames = {"council_id", "material_id"}))
public class CouncilMaterial {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "council_id")
  private Council council;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "material_id")
  private Material material;

  @Enumerated(EnumType.STRING)
  @Column(name = "bin_type", nullable = false, length = 50)
  private BinType binType;

  @Column(columnDefinition = "TEXT")
  private String instructions;

  @Column(columnDefinition = "TEXT")
  private String notes;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  public CouncilMaterial() {}

  @PrePersist
  protected void onCreate() {
    createdAt = LocalDateTime.now();
  }

  public enum BinType {
    RECYCLING,
    GENERAL_WASTE,
    GREEN_WASTE,
    SOFT_PLASTICS,
    SPECIAL_DROP_OFF,
    NOT_ACCEPTED
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public Council getCouncil() {
    return council;
  }

  public void setCouncil(Council council) {
    this.council = council;
  }

  public Material getMaterial() {
    return material;
  }

  public void setMaterial(Material material) {
    this.material = material;
  }

  public BinType getBinType() {
    return binType;
  }

  public void setBinType(BinType binType) {
    this.binType = binType;
  }

  public String getInstructions() {
    return instructions;
  }

  public void setInstructions(String instructions) {
    this.instructions = instructions;
  }

  public String getNotes() {
    return notes;
  }

  public void setNotes(String notes) {
    this.notes = notes;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public void setCreatedAt(LocalDateTime createdAt) {
    this.createdAt = createdAt;
  }
}
